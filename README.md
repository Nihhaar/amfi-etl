# AMFI ETL

## Run (Virtualenv)
```bash
virtualenv -p /usr/local/opt/python@3.9/bin/python3.9 .venv
pip3 install -r requirements.txt

# Start MySQL
docker-compose -f docker-compose.yml up -d

# Full load (took 34 mins on my 8GB machine with 8 threads)
# See status at: https://127.0.0.1:8787/status
python3 amfi/main.py full_refresh

# Incremental load
python3 amfi/main.py 2022-01-02
```
