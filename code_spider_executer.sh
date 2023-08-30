#!/bin/bash

for ((i = 1; i <= $#; i++ )); do
  # Activate the virtual environment
  source Scrapy/${!i}/bin/activate

  # Change to the directory containing the Python script
  cd Scrapy/${!i}Spider

  # Run the Python script
  python3 code_spider_runner.py

  cd ../..
done