import time
import argparse
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine

import dask
from dask.distributed import Client, LocalCluster

from conf import settings
from models.amfi import NAV, Base
from parsers.AMFIParser import AMFIParser


def load_data(conn_str, from_date, to_date=None):
    # Get data from API
    amfi_parser = AMFIParser(settings.API_URL, from_date=from_date, to_date=to_date)
    rows = []
    for row in amfi_parser.parse():
        rows.append(row)

    # Write to DB
    if rows:
        engine = create_engine(conn_str, connect_args={"timeout": 15})
        engine.execute(NAV.__table__.insert(), rows)


def setup_dask_cluster():
    dask.config.set({"distributed.worker.memory.terminate": False})
    worker_kwargs = {
        "memory_target_fraction": False,
        "memory_spill_fraction": False,
        "memory_pause_fraction": False,
    }
    cluster = LocalCluster(n_workers=2, threads_per_worker=16, **worker_kwargs)
    client = Client(cluster)
    print(f"Serving dask dashboard at {client.dashboard_link}")
    return client


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def full_load(conn_str):
    # Setup table if not present
    engine = create_engine(conn_str)
    Base.metadata.create_all(engine)

    client = setup_dask_cluster()
    parts = []
    for from_date in daterange(date(2000, 1, 1), date(2022, 1, 1)):
        parts.append(dask.delayed(load_data)(conn_str, from_date))
    dask.compute(parts)
    client.shutdown()


def main():
    # CLI
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "nav_date",
        help="Date in format YYYY-MM-DD for load on that day or 'full_refresh' for a full load",
    )
    args = parser.parse_args()
    nav_date = args.nav_date

    # SQLite
    conn_str = "sqlite:///nav.db"

    # Full refresh
    if nav_date == "full_refresh":
        full_load(conn_str)
        return

    # Incremental load
    from_date = None
    try:
        from_date = datetime.strptime(nav_date, "%Y-%m-%d").date()
    except Exception as e:
        print(f"Invalid date for format YYYY-MM-DD: {nav_date}")
        raise e

    print(f"Loading data for {from_date.strftime('%Y-%m-%d')}")
    load_data(conn_str, from_date)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    minutes, seconds = divmod((end - start), 60)
    print(f"Execution completed in {int(minutes)}.{int(seconds)} minutes")
