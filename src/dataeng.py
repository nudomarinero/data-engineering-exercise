import json
from pathlib import Path
from io import StringIO, BytesIO
from astropy.table import Table
import click
import numpy as np
import requests
from validators import url


class Loader:
    """Class to load the csv data"""
    
    def __init__(self, location, columns=None, lazy=False):
        """Get the csv (dirty) data in memory and perform some validation"""
        self.columns = columns
        self.location_type = location_type(str(location))
        self.location = location

        # Initial validation and load of header
        self._load_head()
        if self.header is None:
            raise ValueError("File or URL cannot be loaded")
        
        # Get columns and verify
        self.header_columns = (e.strip() for e in self.header.split(","))
        if columns is not None:
            for column in columns:
                if column not in self.header_columns:
                    raise ValueError(f"Column {column} cannot be found in the CSV header")
        
        # Actually load data
        if not lazy:
            self.load_data()
        
    def load_data(self):
        """Load data in the most efficient way"""
        # Configuration of the data reader
        kargs_read = {"format": 'ascii.csv'}
        if self.columns is not None:
            kargs_read.update({"include_names": self.columns})
        # Actually load the data
        if self.location_type == "url":
            self.data = Table.read(
                    BytesIO(requests.get(self.location, allow_redirects=True).content), 
                    **kargs_read
                )
        elif self.location_type == "file":
            self.data = Table.read(self.location, **kargs_read)
        else:
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
    return np.quantile(data_column, quantile)


@click.command()
@click.argument("filename")
def cli(filename):
    try:
        data = Loader(filename, columns=["trip_distance"]).data["trip_distance"]
        result = compute_quantile(data)
        output = {"status": "OK", "result": result}
        print(json.dumps(output))
    except Exception as e:
        output = {"status": "failed", "exception": repr(e)}
    print(json.dumps(output))
