# kuchniowy-raj
Projekt PPZ

### Uruchomienie:
Najlepiej uruchamiać w wirtualnym środowisku
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Wersja developerska
```bash
python3 run.py
```

#### Wersja produkcyjna
```bash
gunicorn \
    --bind localhost:8000 \
    --pid app.pid \
    --workers 2 \
    --daemon \
    --access-logfile logs/gunicorn.log \
    run
```
