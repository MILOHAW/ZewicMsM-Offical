import sys
sys.path.insert(0, r'E:\Next-Private-Server-main\My Singing Monsters Server')
import msm_store
msm_store.db_dir = r'E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\db_files'
msm_store.players_dir = r'E:\Next-Private-Server-main\My Singing Monsters Server\SFS2X\extensions\MSM\players'
from msm_monsters import viewed_egg
from msm_playerdata import load_player

root, player = load_player('Nextstars')
for island in player.get('islands', []) or []:
    eggs = island.get('eggs') or []
    if eggs:
        for egg in eggs[:5]:
            uid = egg.get('user_egg_id')
            print('EGG', uid, 'monster', egg.get('monster'), 'structure', egg.get('structure'))
            try:
                result = viewed_egg('Nextstars', {'user_egg_id': uid})
                print('RESULT', result)
            except Exception as e:
                import traceback; traceback.print_exc()
        break
else:
    print('NO EGGS')
