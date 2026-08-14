import msm_protocol
import msm_handlers
import msm_store


def test_raw_frame_round_trip_for_gs_player():
    payload = {"player_object": {"username": "Nextstars"}}
    frame = msm_protocol.build_raw_frame("gs_player", payload)
    parsed = msm_protocol.parse_raw_frame(frame)
    assert parsed is not None
    assert parsed.command == "gs_player"
    assert parsed.params == payload


def test_gs_create_clubbox_creates_persistent_player_clubbox(tmp_path, monkeypatch):
    monkeypatch.setattr(msm_store, "players_dir", str(tmp_path))
    player_root = {"player_object": {"active_island": 12345, "islands": [{"user_island_id": 12345}]}}
    msm_store.save_user_data("Nextstars", player_root)

    result = msm_handlers.handle_command("gs_create_clubbox", {"act": 7})

    assert result and result[0][0] == "gs_create_clubbox"
    assert result[0][1]["success"] is True
    saved = msm_store.load_user_data("Nextstars")
    clubboxes = saved["player_object"].get("clubboxes") or []
    assert any(item.get("act") == 7 for item in clubboxes)
    assert clubboxes[-1]["clubbox_data"]["island"] == 12345
