#!/usr/bin/env python3
"""Set player level to 100 and persist it."""
import json
from pathlib import Path

def set_level_100():
    player_file = Path(r"e:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players\Nextstars.json")
    
    # Load current player data
    with open(player_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    player_object = data.get('player_object', {})
    
    # Set level to 100
    player_object['level'] = 100
    if 'profile' in player_object and isinstance(player_object['profile'], dict):
        player_object['profile']['level'] = 100
    
    # Update all islands' last_player_level
    for island in player_object.get('islands', []):
        if isinstance(island, dict):
            island['last_player_level'] = 100
    
    # Write back
    data['player_object'] = player_object
    with open(player_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Set level to 100")
    print(f"✓ Saved to {player_file}")
    print(f"File size: {player_file.stat().st_size} bytes")
    
    # Verify
    with open(player_file, 'r', encoding='utf-8') as f:
        verify_data = json.load(f)
    verify_level = verify_data.get('player_object', {}).get('level')
    print(f"✓ Verification: Player level is now {verify_level}")

if __name__ == '__main__':
    set_level_100()
