# Eml2Tex

Eml2Tex is a simple Python script that converts an email message to a LaTeX file. It is useful for converting emails to LaTeX files for academic purposes.

## Installation

To install Eml2Tex, simply clone the repository and run the following command:

```bash
poetry install
```

## Usage

To use Eml2Tex, you have to run 2 scripts:

1. Run the following command to convert the email message to a JSON file:

```bash
python eml2json.py <email1.eml> <email2.eml> ...
```

2. Run the following command to convert the JSON file to a LaTeX file:

```bash
python json2tex.py <email1.json> <email2.json> ...
```
