#!/usr/bin/env python3
"""
Create player save files for all accounts in Accounts.json to enable multiplayer.
"""

import json
import sys
from pathlib import Path

# Set up paths
sys.path.insert(0, '.')
import msm_store

msm_store.db_dir = Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\db_files")
msm_store.players_dir = Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players")

def create_player_saves_from_accounts():
    """Create player save files for all accounts in Accounts.json"""
    
    accounts_file = Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\Accounts.json")
    
    if not accounts_file.exists():
        print(f"ERROR: Accounts.json not found at {accounts_file}")
        return False
    
    # Load accounts
    with open(accounts_file, "r", encoding="utf-8") as f:
        accounts = json.load(f)
    
    if not accounts:
        print("ERROR: No accounts found in Accounts.json")
        return False
    
    # Load template from Nextstars
    try:
        template_root = msm_store.load_user_data("Nextstars")
    except Exception as e:
        print(f"ERROR: Could not load Nextstars template: {e}")
        return False
    
    print(f"Loaded Nextstars template")
    print(f"Creating player files for {len(accounts)} accounts...\n")
    
    created = 0
    failed = 0
    skipped = 0
    
    players_dir = msm_store.players_dir
    
    for i, account in enumerate(accounts, 1):
        username = account.get("username")
        user_id = account.get("user_id")
        user_game_id = account.get("user_game_id")
        
        if not username:
            print(f"  [{i}/{len(accounts)}] SKIPPED: Account has no username")
            skipped += 1
            continue
        
        player_file = players_dir / f"{username}.json"
        
        # Skip if already exists
        if player_file.exists():
            print(f"  [{i}/{len(accounts)}] {username:30s} - ALREADY EXISTS")
            skipped += 1
            continue
        
        try:
            # Create player from template
            root = json.loads(json.dumps(template_root))  # Deep copy
            player_obj = root.get("player_object", {})
            
            # Update player info
            player_obj["username"] = username
            player_obj["user_id"] = user_id or username
            player_obj["user_game_id"] = user_game_id or username
            player_obj["bbb_id"] = user_id or username
            
            root["player_object"] = player_obj
            
            # Save
            msm_store.save_user_data(username, root)
            print(f"  [{i}/{len(accounts)}] {username:30s} - CREATED")
            created += 1
            
        except Exception as e:
            print(f"  [{i}/{len(accounts)}] {username:30s} - ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Completed!")
    print(f"  Successfully created: {created}")
    print(f"  Skipped (already exist): {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(accounts)}")
    print(f"\n✅ Multi-player setup complete!")
    print(f"Players are now ready to connect with their respective accounts.")
    
    return failed == 0

if __name__ == "__main__":
    success = create_player_saves_from_accounts()
    sys.exit(0 if success else 1)
