import json

store_data = json.load(open(r'Data\db_files\db_store_v2.json'))
castle_items = [i for i in store_data.get('store_item_data', []) if 'castle' in str(i).lower()]

if castle_items:
    c = castle_items[0]
    print(f"Castle item verified:")
    print(f"  group_id: {c.get('group_id')} (structures)")
    print(f"  structure_id: {c.get('structure_id')}")
    print(f"  enabled: {c.get('enabled')}")
    print(f"  has_contents: {'contents' in c}")
    print(f"  price: {c.get('price')} {c.get('currency')}")
