import sqlite3
from dotenv import find_dotenv, load_dotenv
import os
import json

load_dotenv(find_dotenv())

HERO_CHARACTERISTICS_KEYS = [
    "hero_id", "name", "localized_name", "primary_attr", "attack_type",
    "roles", "base_health", "base_health_regen", "base_mana", "base_mana_regen",
    "base_armor", "base_mr", "base_attack_min", "base_attack_max", "base_str", "base_agi",
    "base_int", "str_gain", "agi_gain", "int_gain", "attack_range", "projectile_speed",
    "attack_rate", "move_speed", "turn_rate", "cm_enabled", "legs", "pro_ban", "pro_win",
    "pro_pick", "pick_1", "win_1", "pick_2", "win_2", "pick_3", "win_3", "pick_4", "win_4",
    "pick_5", "win_5", "pick_6", "win_6", "pick_7", "win_7", "pick_8", "win_8", "null_pick"
]

def to_row(char) -> tuple:
    modified = char | {
        "roles": ",".join(char["roles"]), "pick_1": char["1_pick"], "win_1": char["1_win"],
        "pick_2": char["2_pick"], "win_2": char["2_win"], "pick_3": char["3_pick"],
        "win_3": char["3_win"], "pick_4": char["4_pick"], "win_4": char["4_win"],
        "pick_5": char["5_pick"], "win_5": char["5_win"], "pick_6": char["6_pick"],
        "win_6": char["6_win"], "pick_7": char["7_pick"], "win_7": char["7_win"],
        "pick_8": char["8_pick"], "win_8": char["8_win"]
    }

    return tuple(modified[k] for k in HERO_CHARACTERISTICS_KEYS)

if __name__ == "__main__":
    hero_characteristics = json.load(open('datasets/external/hero_characteristics.json'))

    # database connections
    conn = sqlite3.connect(os.environ.get("SQLITE_DATABASE_URL"))
    c = conn.cursor()

    # prepare the query
    placeholders = ",".join(["?"] * len(HERO_CHARACTERISTICS_KEYS))
    insert_query = 'INSERT INTO hero_characteristics(%s) VALUES(%s);' % (
        ",".join(HERO_CHARACTERISTICS_KEYS), placeholders
    )

    # execute the query
    c.executemany(insert_query, [to_row(d) for d in hero_characteristics]);
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()
