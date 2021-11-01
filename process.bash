#!/bin/bash
while IFS= read -r line; do
    echo "File: $line";
    poetry run compute_yellow $line;
done < list_csv.txt