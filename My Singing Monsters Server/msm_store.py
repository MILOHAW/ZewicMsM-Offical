import json
import time
import logging
from pathlib import Path

from msm_protocol import SFSLong

logger = logging.getLogger('msm.store')
db_dir = None
players_dir = None

_db_cache = {}



_UNCACHED_DB_NAMES = {"gs_timed_events"}


def _candidate_db_dirs():
    seen = set()
    candidates = []

    def add(path):
        if path is None:
            return
        resolved = Path(path).resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        candidates.append(resolved)

    add(Path(r"E:\Next-Private-Server-main\Data\db_files"))
    add(Path(r"D:\Next-Private-Server-main\Data\db_files"))
    add(db_dir if db_dir is not None else Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\db_files"))
    add(Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\db_files"))
    add(Path(r"D:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\db_files"))
    add(Path(r"D:\Next-Private-Server-main\My Singing Monsters Server\db_files"))
    add(Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\db_files"))
    return candidates


def load_db_json(name):
    if name in _db_cache:
        return _db_cache[name]

    for directory in _candidate_db_dirs():
        path = directory / f"{name}.json"
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8-sig") as fh:
                data = json.load(fh)
        except Exception:
            if name in _UNCACHED_DB_NAMES:
                return None
            _db_cache[name] = None
            return None
        if name not in _UNCACHED_DB_NAMES:
            _db_cache[name] = data
        return data

    if name in _UNCACHED_DB_NAMES:
        return None
    _db_cache[name] = None
    return None


def normalize_db_payload(command, payload):
    now_ms = SFSLong(int(time.time() * 1000))
    payload.setdefault("server_time", now_ms)
    payload.setdefault("last_updated", now_ms)
    if command.startswith("gs_"):
        payload.setdefault("success", True)
    return payload


def _candidate_players_dirs():
    seen = set()
    candidates = []

    def add(path):
        if path is None:
            return
        resolved = Path(path).resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        candidates.append(resolved)

    add(players_dir if players_dir is not None else Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players"))
    add(Path(r"E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players"))
    add(Path(r"D:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players"))
    add(Path(r"E:\Next-Private-Server-main\Captures"))
    add(Path(r"D:\Next-Private-Server-main\My Singing Monsters Server\players"))
    return candidates


def _player_file(username):
    if players_dir is None:
        raise RuntimeError("msm_store.players_dir not configured")
    return Path(players_dir) / f"{username}.json"


def _normalize_player_account(root):
    if not isinstance(root, dict):
        return root
    player_object = root.get("player_object")
    if not isinstance(player_object, dict):
        return root

    player_object["premium"] = 999_999_999
    player_object["has_premium"] = True
    player_object["is_premium"] = True
    player_object["premium_status"] = "premium"

    try:
        from msm_gamedata import all_monster_ids, monster_ids_allowed_on_island
        from msm_monsters import MAGICAL_NEXUS_ISLAND_TYPE, grant_full_book, island_type_of, repair_book_of_monsters_counts
    except Exception:
        return root

    for island in player_object.get("islands") or []:
        if not isinstance(island, dict):
            continue
        grant_full_book(island)
        island["book_value"] = 3334

    return root


def load_user_data(username):
    for directory in _candidate_players_dirs():
        path = directory / f"{username}.json"
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8-sig") as fh:
                data = json.load(fh)
            return _normalize_player_account(data)
        except Exception:
            continue

    raise FileNotFoundError(f"no player data for {username!r} in any of {[str(d) for d in _candidate_players_dirs()]}")


def save_user_data(username, root):
    root = _normalize_player_account(root)
    
    # Try all candidate directories
    for directory in _candidate_players_dirs():
        path = directory / f"{username}.json"
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as fh:
                json.dump(root, fh)
            return  # Success
        except Exception as e:
            continue  # Try next directory
    
    # Fallback: if nothing worked, try the configured players_dir
    if players_dir is None:
        raise RuntimeError("msm_store.players_dir not configured and all candidate directories failed")
    path = _player_file(username)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(root, fh)
