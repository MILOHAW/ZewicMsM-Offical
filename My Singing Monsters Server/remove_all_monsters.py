#!/usr/bin/env python3
"""Remove all monsters from all islands."""
import json
from pathlib import Path

def remove_all_monsters():
    player_file = Path(r"e:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players\Nextstars.json")
    
    # Load current player data
    with open(player_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    player_object = data.get('player_object', {})
    
    # Clear monsters from all islands
    total_removed = 0
    for island in player_object.get('islands', []):
        if isinstance(island, dict):
            monster_count = len(island.get('monsters', []))
            island['monsters'] = []
            total_removed += monster_count
            print(f"  Island {island.get('user_island_id')}: removed {monster_count} monsters")
    
    # Write back
    data['player_object'] = player_object
    with open(player_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Removed {total_removed} total monsters")
    print(f"✓ Saved to {player_file}")
    
    # Verify
    with open(player_file, 'r', encoding='utf-8-sig') as f:
        verify_data = json.load(f)
    for island in verify_data.get('player_object', {}).get('islands', []):
        monster_count = len(island.get('monsters', []))
        if monster_count > 0:
            print(f"❌ WARNING: Island {island.get('user_island_id')} still has {monster_count} monsters")
    print("✓ Verification complete")

if __name__ == '__main__':
    remove_all_monsters()
