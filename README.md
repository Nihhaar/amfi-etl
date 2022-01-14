# AMFI ETL
Data ingestion pipeline to fetch Mutual Fund data from the [AMFI](https://www.amfiindia.com/nav-history-download) website, model, and store that data into a database for further processing.
### Run (Virtualenv)
```bash
virtualenv -p /usr/local/opt/python@3.9/bin/python3.9 .venv
source .venv/bin/activate
pip3 install -r requirements.txt # make sure you have mysql libs installed

# Start MySQL
docker-compose -f docker-compose.yml up -d

# Full load (took 34 mins on my 8GB machine with 8 threads)
# See status at: https://127.0.0.1:8787/status
python3 amfi/main.py full_refresh

# Incremental load
python3 amfi/main.py 2022-01-02
```

### Checklist
- [x] Full load
- [x] Incremental load every day
- [x] Performance efficient (Full load takes 34 mins < 3hrs)
- [x] MySQL with Docker
- [ ] Dimenstional Modeling for query performance