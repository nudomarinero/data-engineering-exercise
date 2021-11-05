#!/bin/bash
while IFS= read -r line; do
    echo "File: $line";
    name=$(echo $(echo $line | cut -d/ -f6) | cut -d. -f1)
    poetry run compute_yellow $line > ${name}-processed.csv;
done < list_csv.txt