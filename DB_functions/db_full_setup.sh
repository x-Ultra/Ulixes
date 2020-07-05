#!/bin/sh
python3 create_table.py
echo "table created"
python3 insert_items.py
echo "itineraries iserted"
