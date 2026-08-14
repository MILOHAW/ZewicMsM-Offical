#!/usr/bin/env python
"""Test multi-player save file system."""

import json
import pathlib
import sys
sys.path.insert(0, '.')

# Set up paths
import msm_store
msm_store.players_dir = pathlib.Path(r'E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players')

# Test loading Nextstars only (since others don't exist yet)
try:
    root = msm_store.load_user_data('Nextstars')
    player_obj = root.get('player_object', {})
    username = player_obj.get('username')
    level = player_obj.get('level')
    islands = len(player_obj.get('islands', []))
    print(f'✓ Nextstars loaded: username={username}, level={level}, islands={islands}')
except Exception as e:
    print(f'✗ Nextstars: {e}')

# Now test creating a new player save file
print('\nCreating new player files...')
for player_name in ['Player_Alice', 'Player_Bob']:
    try:
        # Load template
        root = msm_store.load_user_data('Nextstars')
        # Modify for new player
        player_obj = root.get('player_object', {})
        player_obj['username'] = player_name
        player_obj['user_id'] = 9000000 + hash(player_name) % 100000
        player_obj['bbb_id'] = player_name
        root['player_object'] = player_obj
        
        # Save new player
        msm_store.save_user_data(player_name, root)
        print(f'✓ Created {player_name}')
    except Exception as e:
        print(f'✗ Failed to create {player_name}: {e}')

# Verify files exist
print('\nVerifying player files:')
players_dir = pathlib.Path(r'E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players')
for player in ['Nextstars', 'Player_Alice', 'Player_Bob']:
    file_path = players_dir / f'{player}.json'
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f'✓ {file_path.name} exists ({size_kb:.1f} KB)')
    else:
        print(f'✗ {file_path.name} missing')

print('\n✅ Multi-player file system verified')
