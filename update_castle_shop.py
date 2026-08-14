import json

# Load structure database to find a generic castle
struct_data = json.load(open(r'Data\db_files\db_structure.json', encoding='utf-8'))
structs = struct_data.get('structures_data', [])

# Find a generic castle - CASTLE_01 (ID 7) is the most basic
castle_struct = next((s for s in structs if s.get('structure_id') == 7), None)

if castle_struct:
    print(f"Using castle: ID={castle_struct.get('structure_id')}, name={castle_struct.get('name')}")
    print(f"  cost={castle_struct.get('cost')}")
    print(f"  currency={castle_struct.get('currency')}")
    print(f"  is_purchasable={castle_struct.get('purchasable', castle_struct.get('is_purchasable'))}")
else:
    print("Castle 7 not found")

# Now update the shop to use this castle
store_data = json.load(open(r'Data\db_files\db_store_v2.json', encoding='utf-8'))
items = store_data.get('store_item_data', [])

# Find the castle we just added
castle_item = next((i for i in items if i.get('item_name') == 'castle.structure'), None)

if castle_item:
    castle_item['contents'] = [
        {
            "type": "STRUCTURE",
            "id": 7,
            "debug": "castle_01_generic"
        }
    ]
    
    # Save
    with open(r'Data\db_files\db_store_v2.json', 'w', encoding='utf-8') as f:
        json.dump(store_data, f, ensure_ascii=False, separators=(',', ': '))
    
    print(f"Updated shop item to use generic CASTLE_01 (ID 7)")
