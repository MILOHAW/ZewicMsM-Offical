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
    base_dir = Path(__file__).resolve().parent

    def add(path):
        if path is None:
            return
        resolved = Path(path).resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        candidates.append(resolved)

    add(base_dir / "db_files")
    add(base_dir / "Data" / "db_files")
    add(base_dir.parent / "Data" / "db_files")
    add(base_dir.parent / "db_files")
    if db_dir is not None:
        add(Path(db_dir))
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
    base_dir = Path(__file__).resolve().parent

    def add(path):
        if path is None:
            return
        resolved = Path(path).resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        candidates.append(resolved)

    add(base_dir / "SFS2X" / "extensions" / "MSM" / "players")
    add(base_dir / "players")
    add(base_dir.parent / "Captures")
    add(base_dir.parent / "players")
    if players_dir is not None:
        add(Path(players_dir))
    return candidates


def _player_file(username):
    if players_dir is None:
        raise RuntimeError("msm_store.players_dir not configured")
    return Path(players_dir) / f"{username}.json"
 

def _sanitize_debug_player_data(player_object):
    if not isinstance(player_object, dict):
        return

    for key in ("premium", "premium_status", "has_premium", "is_premium"):
        if key in player_object:
            value = player_object.get(key)
            if key == "premium" and isinstance(value, (int, float)) and int(value) >= 999_000_000:
                player_object.pop(key, None)
                continue
            if key in {"has_premium", "is_premium"} and value is True:
                player_object.pop(key, None)
                continue
            if key == "premium_status" and value == "premium":
                player_object.pop(key, None)
                continue

    for key in ("xp", "coins", "diamonds", "food", "ethereal_currency", "keys", "relics", "egg_wildcards", "clubbox_tokens", "starpower"):
        if key in player_object and isinstance(player_object.get(key), (int, float)) and int(player_object[key]) >= 999_000_000:
            player_object[key] = 0

    for key in ("coins_actual", "diamonds_actual", "food_actual", "ethereal_currency_actual", "keys_actual", "relics_actual", "egg_wildcards_actual", "clubbox_tokens_actual", "starpower_actual"):
        if key in player_object and isinstance(player_object.get(key), (int, float)) and int(player_object[key]) >= 999_000_000:
            player_object[key] = 0


def _normalize_player_account(root):
    if not isinstance(root, dict):
        return root
    player_object = root.get("player_object")
    if not isinstance(player_object, dict):
        return root

    _sanitize_debug_player_data(player_object)
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
