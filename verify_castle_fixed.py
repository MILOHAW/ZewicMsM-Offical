import json

# Verify both databases
s = json.load(open('Data/db_files/db_structure.json'))
c = [x for x in s['structures_data'] if x.get('structure_id') == 7][0]
print(f'Castle structure (ID 7):')
print(f'  view_in_market: {c["view_in_market"]} ✓' if c["view_in_market"] == 1 else f'  view_in_market: {c["view_in_market"]} ✗')
print(f'  name: {c["name"]}')
print(f'  cost: {c["cost_coins"]} coins')

st = json.load(open('Data/db_files/db_store_v2.json'))
it = [x for x in st['store_item_data'] if 'castle' in str(x).lower()][0]
print(f'\nCastle shop item:')
print(f'  group_id: {it["group_id"]} (structures section)')
print(f'  structure_id: {it["structure_id"]}')
print(f'  enabled: {it["enabled"]}')
print(f'  price: {it["price"]} {it["currency"]}')

if c['view_in_market'] == 1 and it['group_id'] == 7 and it['enabled'] == 1:
    print('\n✅ All configurations correct! Castle should now appear in the shop.')
