# Python Server

Cd into pose-score-service and run the following command (as appropriate to your computer)

## Create Virtual enviroment

[Visual Studio Guide to virtaul enviroments](https://code.visualstudio.com/docs/python/environments)

### macOS/Linux

You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs

```python3 -m venv .venv```

### Windows

You can also use `py -3 -m venv .venv`

```python -m venv .venv```

## To activate the virtual environment

### Linux
```source .venv/bin/activate```

### Windows

```venv\scripts\activate```

## To install requirements 

```pip install -r requirements.txt```

or

```pip3 install -r requirements.txt```

## To start python server , run 

```python app.py```

If working, “Running on http://127.0.0.1:5000 (Press CTRL+C to quit)” will be printed in the terminal