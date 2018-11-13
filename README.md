# Spelling Practice

Game to practice acronym spelling.

It uses the Google Translate API to say a random acronym that you then have to write.

## Installation

1. Clone this repo.
2. Use Python 3.6 and install the requirements:

```bash
pip install -r requirements.txt
``` 

## Run

Needs Internet connection to run:

```bash
./main.py
```

It will provide random acronyms of length 5 in English.

## Options

Here there are some useful options to change.

### Slow mode

```bash
./main.py --slow
```

### Practice with numbers

```bash
./main.py --add-number
```

### Use Spanish

```bash
./main.py --lang es --alphabet ABCDEFGHIJKLMNÑOPQRSTUVWXYZ
```

### More

To see all the available options:

```bash
./main.py -h
```
