from io import StringIO
import json
import logging
from pathlib import Path
import sys
from astropy.table import Table
from astropy.io.ascii import InconsistentTableError
import click
import numpy as np
import requests
from validators import url


logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
log = logging.getLogger(__name__)

class Extractor:
    """Class to perform some validation, and load the CSV in memory. It can also "extract" the data if an URL is provided.
    """
    
    def __init__(self, location, check_columns=None, lazy=False):
        """Get the csv (dirty) data in memory and perform some validation"""
        self.check_columns = check_columns
        self.location_type = location_type(str(location))
        self.location = location

        # Initial validation and load of header
        log.debug(f"Load header of {self.location}")
        self._load_head()
        if self.header is None:
            log.error("File or URL cannot be found")
            raise ValueError("File or URL cannot be found")
        
        # Get columns and verify
        log.debug(f"Verify that the columns are in the header")
        self.header_columns = (e.strip() for e in self.header.split(","))
        if check_columns is not None:
            for column in check_columns:
                if column not in self.header_columns:
                    log.warn(f"Column {column} is not in the header")
        
        # Actually load data
        if not lazy:
            self.load_data()
        
    def load_data(self):
        """Load data into table in memory"""
        # Actually load the data
        if self.location_type in ["url", "file"]:
            log.info("Start data loading")
            try:
                self.data = Table.read(self.location, format='ascii.csv')
            except InconsistentTableError as e:
                log.error(f"Error loading CSV data: {repr(e)}")
                self.data = None
        else:
            log.warn(f"Data cannot be loaded from {self.location}")
            self.data = None

    def _load_head(self):
        """Loads the first lines of the file and verify that the data is there"""
        if self.location_type == "url":
            self.head = load_header_url(self.location)
            self.header = self.head[0]
        elif self.location_type == "file":
            self.head = load_header_file(self.location)
            self.header = self.head[0]
        else:
            self.head = None
            self.header = None


def load_header_url(url, max_bytes=1024):
    """Load the first line or first 1024 bytes from a URL"""
    with StringIO(requests.get(
            url, 
            allow_redirects=True, 
            headers={'Range' : f'bytes=0-{max_bytes}'}
        ).content.decode("utf8")) as data_in:
            lines = data_in.readlines()
            return [line.strip() for line in lines]


def load_header_file(file_path):
    """Load the first line of a local file"""
    with open(Path(file_path)) as data_in:
        lines = data_in.readlines()
        return [line.strip() for line in lines]


def location_type(location):
    """Get the type of location"""
    if url(location):
        return "url"
    elif Path(location).is_file():
        return "file"
    else:
        return "unknown"


def compute_quantile(data_column, quantile=0.9):
    log.debug(f"Start compute quantile {quantile}")
    q = np.quantile(data_column, quantile)
    log.debug(f"Quantile result for column: {q}")
    return q


@click.command()
@click.argument("filename")
def cli(filename):
    try:
        data = Extractor(filename, check_columns=["trip_distance"]).data
        result = compute_quantile(data["trip_distance"])
        log.info("Status: OK")
        data[data["trip_distance"] >= result].write(sys.stdout, format='csv')
        
    except Exception as e:
        log.info("Status: Failed")
        log.info(f"Exception: {repr(e)}")
        raise e

