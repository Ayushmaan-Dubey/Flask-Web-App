# Flask Web App

Quick dev run instructions

1. Activate the project virtualenv (macOS / zsh):

```zsh
source "/Users/ayushmaandubey/flask-env/bin/activate"
```

2. Run the app (default port 5000):

```zsh
python main.py
```

3. If port 5000 is already in use, set a different port and run:

```zsh
export PORT=5001
python main.py
```

Troubleshooting

- If you see "ModuleNotFoundError: No module named 'flask'", make sure the venv is activated and Flask is installed in it:

```zsh
python -m pip install flask
```

- If the navbar toggler doesn't expand, try disabling `static/script.js` temporarily (it may throw a JS error). Open DevTools → Console to see errors.
