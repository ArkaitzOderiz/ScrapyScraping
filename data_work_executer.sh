#!/bin/bash

for ((i = 1; i <= $#; i++ )); do
  # Activate the virtual environment
  source Scrapy/${!i}/bin/activate

  # Change to the directory containing the Python script
  cd Scrapy/${!i}Spider

  # Run the Python script
  python3 TrabajarJSONs/formatear_data_JSONs.py
  python3 TrabajarJSONs/filtrar_data_JSONs.py

  cd ../..
done