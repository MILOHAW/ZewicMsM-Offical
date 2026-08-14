#!/usr/bin/env python3
"""Find castle structure ID."""
import json

with open(r'E:\Next-Private-Server-main\Data\db_files\db_structure.json') as f:
    data = json.load(f)

castles = [s for s in data.get('structures_data', []) if 'castle' in str(s.get('name', '')).lower()]
if castles:
    print("Castles found:")
    for c in castles:
        print(f"  ID: {c.get('structure_id')}, Name: {c.get('name')}, Level: {c.get('level')}")
else:
    print("No castles found. Available structure types:")
    types = set(s.get('structure_type') for s in data.get('structures_data', []))
    for t in sorted(types):
        print(f"  - {t}")
    print("\nSearching for anything with 'castle' in the name:")
    for s in data.get('structures_data', []):
        name = s.get('name', '').lower()
        if 'castle' in name or 'fort' in name:
            print(f"  ID: {s.get('structure_id')}, Name: {s.get('name')}, Level: {s.get('level')}")
