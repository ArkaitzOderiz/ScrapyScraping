#!/bin/bash

# Activate the virtual environment
source Scrapy/$1/bin/activate

# Change to the directory containing the Python script
cd Scrapy/$1Spider

# Run the Python script
python3 code_spider_runner.py