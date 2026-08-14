#!/usr/bin/env python
"""Rebuild Nextstars.json from captured data with all game logic corrections applied."""

import json
import pathlib
import time
from typing import Any, Dict, List

# Load captured player data
cap_file = pathlib.Path(r'E:\Next-Private-Server-main\Captures\1\msm_json\69_gs_player.json')
out_file = pathlib.Path(r'E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players\Nextstars.json')
events_file = pathlib.Path(r'E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\data\gs_timed_events.json')

# Load player from capture
cap_data = json.loads(cap_file.read_text(encoding='utf-8'))
player = cap_data.get('player_object') or cap_data.get('payload', {}).get('player_object')
assert player, 'No player_object found in capture'

print(f"Loaded player: {player.get('username')} (level {player.get('level')}, {len(player.get('islands', []))} islands)")

# ===== APPLY CORRECTIONS =====

# 1. Ensure level is at least reasonable
if player.get('level', 0) < 50:
    print("Boosting level to 50...")
    player['level'] = 50
    if 'profile' in player and isinstance(player['profile'], dict):
        player['profile']['level'] = 50

# 2. Remove monsters and ensure castle_5 on all islands
castles_added = 0
monsters_removed = 0
for island in player.get('islands', []):
    if isinstance(island, dict):
        # Remove monsters
        monster_count = len(island.get('monsters', []))
        island['monsters'] = []
        monsters_removed += monster_count
        
        # Ensure island has required fields
        if 'island_type' not in island:
            island['island_type'] = 1
        
        # Add castle_5 if not present
        has_castle = any(s.get('structure') == 204 for s in island.get('structures', []))
        if not has_castle:
            if 'structures' not in island:
                island['structures'] = []
            castle = {
                "user_structure_id": 1000000 + castles_added,
                "structure": 204,  # CASTLE_05
                "level": 4,
                "island": island.get("user_island_id", 0),
                "x": 0,
                "y": 0,
                "z": 0,
            }
            island['structures'].append(castle)
            castles_added += 1

print(f"Applied: removed {monsters_removed} monsters, added {castles_added} castles")

# 3. Ensure island 1 has all skins free and owned
island_1 = None
for island in player.get('islands', []):
    if isinstance(island, dict) and (island.get('user_island_id') == 1 or island.get('island') == 1):
        island_1 = island
        break

if island_1:
    print("Setting all skins free and owned on island 1...")
    if 'owned_island_themes' not in island_1:
        island_1['owned_island_themes'] = []
    if 'active_island_themes' not in island_1:
        island_1['active_island_themes'] = []
    
    # Unlock common theme IDs (1-10 are usually standard)
    for theme_id in range(1, 11):
        theme_obj = {
            "user_island_theme_id": 1000 + theme_id,
            "island": 1,
            "user_island_id": 1,
            "theme_id": theme_id,
            "skin_id": theme_id,
            "owned": 1,
            "available": 1,
            "cost_diamonds": 0,
        }
        # Avoid duplicates
        if not any(t.get('theme_id') == theme_id for t in island_1['owned_island_themes']):
            island_1['owned_island_themes'].append(theme_obj)
        if not any(t.get('theme_id') == theme_id for t in island_1['active_island_themes']):
            island_1['active_island_themes'].append(theme_obj)
    
    print(f"Island 1 now has {len(island_1['owned_island_themes'])} unlocked themes")

# 4. Enable all timed events if events file exists
if events_file.exists():
    print("Enabling all timed events...")
    events_data = json.loads(events_file.read_text(encoding='utf-8'))
    now_ms = int(time.time() * 1000)
    future_ms = now_ms + (365 * 24 * 3600 * 1000)
    
    events_modified = 0
    for event in events_data.get('timed_event_list', []):
        event['start_date'] = now_ms
        event['end_date'] = future_ms
        event['last_updated'] = now_ms
        events_modified += 1
    
    events_file.write_text(json.dumps(events_data, indent=2), encoding='utf-8')
    print(f"Enabled {events_modified} timed events")
else:
    print(f"Events file not found: {events_file}")

# 5. Save rebuilt player
root = {'player_object': player}
out_file.write_text(json.dumps(root, ensure_ascii=False, indent=2), encoding='utf-8')

print(f"\n✅ Rebuilt Nextstars.json:")
print(f"   username: {player.get('username')}")
print(f"   level: {player.get('level')}")
print(f"   active_island: {player.get('active_island')}")
print(f"   islands: {len(player.get('islands', []))}")
print(f"   saved to: {out_file}")
