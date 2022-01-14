# AMFI ETL

## Run (Virtualenv)
```bash
virtualenv -p /usr/local/opt/python@3.9/bin/python3.9 .venv
pip3 install -r requirements.txt

docker-compose -f docker-compose.yml up -d # start MySQL
python3 amfi/main.py full_refresh # full load (took 34 mins on my 8GB machine with 8 threads)
python3 amfi/main.py 2022-01-02 # incremental load
```
