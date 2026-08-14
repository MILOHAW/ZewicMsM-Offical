import unittest
from pathlib import Path
from unittest import mock

import msm_handlers
import msm_monsters
import msm_store


class HandleCommandFallbackTest(unittest.TestCase):
    def test_db_minigames_missing_returns_success(self):
        result = msm_handlers.handle_command("db_minigames", {})
        self.assertEqual(result, [("db_minigames", {"success": True})])

    def test_db_items_missing_returns_success(self):
        result = msm_handlers.handle_command("db_items", {})
        self.assertEqual(result, [("db_items", {"success": True})])

    def test_gs_quest_missing_returns_safe_payload(self):
        with mock.patch.object(msm_handlers, "load_db_json", return_value={
            "result": [{
                "new": [{
                    "new": 1,
                    "collected": 0,
                    "quest_id": 178,
                    "status": "[true,false]",
                }],
                "next": [{"quest": "GET_M_ABC_ON6"}],
            }]
        }):
            result = msm_handlers.handle_command("gs_quest", {})
        self.assertEqual(result, [("gs_quest", {"success": True, "result": []})])

    def test_viewed_egg_persists_state_and_returns_real_payload(self):
        root = {
            "player_object": {
                "username": "tester",
                "active_island": 101,
                "islands": [{
                    "user_island_id": 101,
                    "eggs": [{
                        "user_egg_id": 77,
                        "monster": 3,
                        "structure": 5,
                        "viewed": False,
                        "ready": False,
                    }],
                    "structures": [{"user_structure_id": 5, "viewed": False, "has_egg": False, "occupied": False}],
                    "monster_book": {"commons": []},
                    "monsters": [],
                }],
            }
        }
        temp_dir = Path(__file__).resolve().parent / "tmp_players"
        temp_dir.mkdir(exist_ok=True)
        try:
            old_players_dir = msm_store.players_dir
            msm_store.players_dir = str(temp_dir)
            msm_store.save_user_data("tester", root)

            result, _ = msm_monsters.viewed_egg("tester", {"user_egg_id": 77})

            self.assertTrue(result["success"])
            self.assertEqual(result["user_egg_id"], 77)
            saved = msm_store.load_user_data("tester")
            egg = saved["player_object"]["islands"][0]["eggs"][0]
            self.assertTrue(egg.get("viewed"))
            self.assertTrue(egg.get("ready"))
            structure = saved["player_object"]["islands"][0]["structures"][0]
            self.assertTrue(structure.get("viewed"))
        finally:
            msm_store.players_dir = old_players_dir


if __name__ == "__main__":
    unittest.main()
