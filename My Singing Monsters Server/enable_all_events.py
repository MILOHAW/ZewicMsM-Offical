#!/usr/bin/env python3
"""Enable all timed events."""
import json
import time
from pathlib import Path

def enable_all_events():
    events_file = Path(r'E:\Next-Private-Server-main\Data\db_files\gs_timed_events.json')
    
    # Load events
    with open(events_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    now_ms = int(time.time() * 1000)
    future_ms = now_ms + (365 * 24 * 3600 * 1000)  # 1 year from now
    
    # Enable all events
    events_modified = 0
    for event in data.get('timed_event_list', []):
        old_start = event.get('start_date')
        old_end = event.get('end_date')
        
        event['start_date'] = now_ms
        event['end_date'] = future_ms
        event['last_updated'] = now_ms
        
        events_modified += 1
        event_type = event.get('event_type', 'Unknown')
        event_id = event.get('id', 'N/A')
        print(f"  Event {event_id} ({event_type}): enabled")
    
    # Save back
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    print(f"\n✓ Enabled {events_modified} events")
    print(f"✓ All events now active until 1 year from now")
    print(f"✓ Saved to {events_file}")

if __name__ == '__main__':
    enable_all_events()
