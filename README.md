# kuchniowy-raj
Projekt PPZ

### Uruchomienie:
Najlepiej uruchamiać w wirtualnym środowisku
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Wersja developerska
```bash
python3 -m pip install -r requirements.txt
python3 run.py
```

#### Wersja produkcyjna
```bash
python3 -m pip install -r requirements.txt
gunicorn \
    --bind localhost:5000 \
    --pid app.pid \
    --workers 2 \
    --daemon \
    --access-logfile logs/gunicorn.log \
    run
```
