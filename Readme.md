# IMDB Scraper

## Installation

Use the package manager [pip](https://pip.pypa.io.en.stable/) to install virtualenv.
```bash
pip install virtualenv
```

Open command prompt in the Imdb folder and type the following commands to create the virtual environment.
```bash
virtualenv venv
```

Activate the virtual environment using the following command.

Mac OS / Linux
```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```

Type the following command to install the dependencies.
```bash
pip install -r requiremnts.txt
```

## Usage
Cd into the imdb_scraper folder and type the following command.
```bash
scrapy crawl imdb_spider
```

Cd into the root folder and type the following command to run the data analysis code.
```bash
python data_analysis.py
```