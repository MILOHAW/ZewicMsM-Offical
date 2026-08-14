#!/usr/bin/env python3
"""Recreate Nextstars.json without monsters and add castles."""
import json
from pathlib import Path

def recreate_without_monsters_add_castles():
    player_file = Path(r"e:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players\Nextstars.json")
    
    # Load current player data
    with open(player_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    player_object = data.get('player_object', {})
    
    # Clear monsters from all islands
    total_removed = 0
    castles_added = 0
    
    for island in player_object.get('islands', []):
        if isinstance(island, dict):
            # Remove monsters
            monster_count = len(island.get('monsters', []))
            island['monsters'] = []
            total_removed += monster_count
            
            # Add castles (structure ID 204 = CASTLE_05 Level 4 max level castle)
            if 'structures' not in island:
                island['structures'] = []
            
            # Create a max level castle_5 structure
            castle = {
                "user_structure_id": 1000000 + castles_added,  # Unique ID
                "structure": 204,  # CASTLE_05 Level 4 (max level)
                "level": 4,
                "island": island.get("user_island_id", 0),
                "x": 0,
                "y": 0,
                "z": 0,
            }
            island['structures'].append(castle)
            castles_added += 1
            
            island_id = island.get('user_island_id')
            print(f"  Island {island_id}: removed {monster_count} monsters, added 1 castle")
    
    # Write back
    data['player_object'] = player_object
    with open(player_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Removed {total_removed} total monsters")
    print(f"✓ Added {castles_added} castles")
    print(f"✓ Saved to {player_file}")
    
    # Verify
    with open(player_file, 'r', encoding='utf-8-sig') as f:
        verify_data = json.load(f)
    
    total_monsters = 0
    total_castles = 0
    for island in verify_data.get('player_object', {}).get('islands', []):
        monster_count = len(island.get('monsters', []))
        castle_count = len([s for s in island.get('structures', []) if s.get('structure') == 204])
        total_monsters += monster_count
        total_castles += castle_count
    
    print(f"✓ Verification: {total_monsters} monsters, {total_castles} castles remaining")

if __name__ == '__main__':
    recreate_without_monsters_add_castles()
