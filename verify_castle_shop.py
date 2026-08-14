import json

store_data = json.load(open(r'Data\db_files\db_store_v2.json', encoding='utf-8'))
castle_items = [i for i in store_data.get('store_item_data', []) if 'castle' in str(i).lower()]

print(f"Castle items in store: {len(castle_items)}")
if castle_items:
    latest = castle_items[-1]
    print(f"Latest castle item:")
    print(f"  ID: {latest.get('storeitem_id')}")
    print(f"  Name: {latest.get('item_name')}")
    print(f"  Price: {latest.get('price')} {latest.get('currency')}")
    print(f"  Contents: {latest.get('contents')}")
