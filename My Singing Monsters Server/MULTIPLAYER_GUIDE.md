# Multi-Player Support Guide

## Overview
The My Singing Monsters Server now supports **multiple simultaneous players**. Each player connects independently, loads their own player save file, and maintains separate game state.

## Key Changes Made

### 1. WebSocket Username Tracking (`bridge_core.py`)
- Added `_WEBSOCKET_USERNAMES` dictionary to map WebSocket IDs to player usernames
- When `USER_LOGIN` command is received, username is extracted from params and stored
- Each connection tracks which player is logged in
- Username is passed to all command handlers

### 2. Command Handler Update (`msm_handlers.py`)
- Updated `handle_command(command, params, username=None)` signature
- Accepts optional `username` parameter (defaults to `DEFAULT_USERNAME`)
- All gameplay handlers now receive the correct username for the logged-in player
- Previously: always used "Nextstars" (hardcoded)
- Now: uses the actual logged-in player's username

### 3. Player Data Loading (already working in `msm_store.py`)
- Each player's data is loaded from `{players_dir}/{username}.json`
- System automatically creates/uses files for any username
- Player data is saved independently per username

## Setting Up Multiple Players

### Step 1: Create Player Save Files
Run the provided script to create player files for all accounts:

```bash
python create_multiplayer_saves.py
```

This script:
- Reads all accounts from `Accounts.json`
- Uses `Nextstars.json` as a template
- Creates a `{username}.json` file for each account
- Updates player metadata (username, user_id, bbb_id)

### Step 2: Add More Accounts (Optional)
Edit `Accounts.json` to add new accounts:

```json
{
  "username": "YourPlayerName",
  "email": "yourplayer@local.test",
  "password": "your_password_or_hash",
  "user_id": "00000000999",
  "user_game_id": "YourPlayerName",
  "steam_id": "765600000000000999"
}
```

Then run `create_multiplayer_saves.py` again to create their save files.

### Step 3: Connect Multiple Clients
Each client can now:
1. Connect to the server
2. Log in with their account username and password
3. Play independently with their own save file
4. Have their changes saved automatically

## Account Credentials
Default accounts available in `Accounts.json`:
- Username: `AlexBlaze099`
- Username: `AlexCanyon200`
- Username: `AlexCreek209`
- Username: `AlexMeadow715`
- Username: `AlexRoot599`
- Username: `AlexVine950`
- And more...

(Default password for all accounts: SHA-256 hash of "password")

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WebSocket Connections                     │
├─────────────────────────────────────────────────────────────┤
│  Connection 1          Connection 2          Connection 3   │
│  Player: Alice         Player: Bob           Player: Charlie│
│  ws_id → "Alice"       ws_id → "Bob"        ws_id → "Charlie"
└──────────┬──────────────────┬──────────────────────┬────────┘
           │                  │                      │
           ▼                  ▼                      ▼
  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
  │ handle_command │ │ handle_command │ │ handle_command │
  │ (user="Alice") │ │ (user="Bob")   │ │ (user="Charlie")
  └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
           │                  │                   │
           ▼                  ▼                   ▼
  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
  │ Alice.json     │ │ Bob.json       │ │ Charlie.json   │
  │ Independent    │ │ Independent    │ │ Independent    │
  │ game state     │ │ game state     │ │ game state     │
  └────────────────┘ └────────────────┘ └────────────────┘
```

## Player Data Storage
- Location: `SFS2X/extensions/MSM/players/`
- Files: `{username}.json` for each player
- Each file contains the complete game state for that player
- Files are automatically saved when changes are made
- Each player's changes are isolated to their own file

## Max Concurrent Players
- Default: 480 connections (configurable in `login_bootstrap_frames()`)
- Set via `MAX_CONNECTION_COUNT` in msm_handlers.py

## Disconnect Handling
When a player disconnects:
1. Their username is removed from the connection tracking
2. A snapshot of Nextstars.json is restored (for testing purposes)
3. The connection is closed cleanly

## Testing Multi-Player
1. Start the server: `python bridge_core.py`
2. Connect Player 1 with account "AlexBlaze099"
3. Connect Player 2 (in separate client/window) with account "AlexCanyon200"
4. Both players should see independent game states
5. Changes made by Player 1 don't affect Player 2

## Troubleshooting

**"FileNotFoundError: no player data for USERNAME"**
- Solution: Run `python create_multiplayer_saves.py` to create missing player files

**All connections show as "Nextstars" in logs**
- Solution: Verify WebSocket is receiving `USER_LOGIN` commands with username params
- Check that `_WEBSOCKET_USERNAMES` tracking is working in the logs

**Different players see the same game state**
- Solution: Verify each player's save file exists: `SFS2X/extensions/MSM/players/{username}.json`
- Check that correct username is passed to `handle_command()` in the handler

## Files Modified
- `bridge_core.py`: Added WebSocket username tracking, updated WebSocket handler
- `msm_handlers.py`: Updated `handle_command()` to accept and use username parameter
- `create_multiplayer_saves.py`: New script to create player files from Accounts.json

## Future Enhancements
- Persistent player data between server restarts
- Player-to-player interactions (trading, battling, etc.)
- Server-wide leaderboards
- Social features (friends, clans, etc.)

TESTING
=======

Created test_multiplayer.py to verify:
✓ Nextstars.json template loads correctly
✓ New player files are created with cloned data
✓ Multiple player files coexist
✓ File sizes match (all inherit same template)

Example output:
  Player_Alice.json exists (162.7 KB)
  Player_Bob.json exists (162.7 KB)
  Both have independent game state

FUTURE ENHANCEMENTS
====================

Possible improvements:
- Persistent session storage (map player to connection)
- Cross-device sync (cloud save)
- Friend/multiplayer interactions
- Shared leaderboards
- Account recovery/password reset
- Admin player management tools
"""

if __name__ == '__main__':
    print(__doc__)
