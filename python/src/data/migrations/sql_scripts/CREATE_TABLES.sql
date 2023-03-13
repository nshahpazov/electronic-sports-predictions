CREATE TABLE player_hero_win_rate (
  id INTEGER NOT NULL,
  account_id INTEGER NOT NULL,
  hero_id INTEGER,
  last_played INTEGER,
  games INTEGER,
  win INTEGER,
  with_games INTEGER,
  with_win INTEGER,
  against_games INTEGER,
  against_win INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE mmr_distribution (
  id INTEGER NOT NULL,
  bin INTEGER,
  bin_name INTEGER,
  count INTEGER,
  cumulative_sum INTEGER,
  percentile REAL,
  PRIMARY KEY (id)
);

CREATE TABLE rank_distribution (
  id INTEGER NOT NULL,
  bin INTEGER,
  bin_name INTEGER,
  count INTEGER,
  cumulative_sum INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE hero_stats (
  id INTEGER NOT NULL,
  hero_id INTEGER NOT NULL,
  percentile INTEGER NOT NULL,
  xp_per_min REAL,
  kills_per_min REAL,
  hero_damage_per_min REAL,
  last_hits_per_min REAL,
  hero_healing_per_min REAL,
  tower_damage REAL,
  gold_per_min REAL,
  PRIMARY KEY (id)
);

CREATE TABLE player_match_rating (
  id INTEGER NOT NULL,
  time TEXT,
  competitive_rank INTEGER,
  solo_competitive_rank INTEGER,
  account_id INTEGER,
  match_id INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE player_match_rating_v2 (
  id INTEGER NOT NULL,
  time TEXT,
  competitive_rank INTEGER,
  solo_competitive_rank INTEGER,
  account_id INTEGER,
  match_id INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE player_heroes_ranking (
  id INTEGER NOT NULL,
  card INTEGER,
  rank INTEGER,
  hero_id INTEGER,
  account_id INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE player (
  id INTEGER NOT NULL,
  account_id INTEGER,
  win INTEGER,
  lose INTEGER,
  competitive_rank INTEGER,
  solo_competitive_rank INTEGER,
  mmr_estimate INTEGER,
  mmr_std_dev INTEGER,
  mmr_n INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE match_player (
  id INTEGER NOT NULL,
  match_id INTEGER,
  account_id INTEGER,
  player_slot INTEGER,
  leaver_status INTEGER,
  hero_id INTEGER,
  gold INTEGER,
  deaths INTEGER,
  hero_damage INTEGER,
  last_hits INTEGER,
  denies INTEGER,
  tower_damage INTEGER,
  xp_per_min INTEGER,
  kills INTEGER,
  hero_healing INTEGER,
  assists INTEGER,
  gold_per_min INTEGER,
  level INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE match (
  id INTEGER NOT NULL,
  barracks_status_dire INTEGER,
  match_id INTEGER,
  duration INTEGER,
  radiant_win BOOLEAN,
  tower_status_dire INTEGER,
  tower_status_radiant INTEGER,
  human_players INTEGER,
  start_time INTEGER,
  game_mode INTEGER,
  PRIMARY KEY (id)
);

CREATE TABLE hero_characteristics (
  id INTEGER NOT NULL,
  hero_id INTEGER,
  name TEXT,
  localized_name TEXT,
  primary_attr TEXT,
  attack_type TEXT,
  roles TEXT,
  base_health REAL,
  base_health_regen REAL,
  base_mana REAL,
  base_mana_regen REAL,
  base_armor REAL,
  base_mr REAL,
  base_attack_min REAL,
  base_attack_max REAL,
  base_str REAL,
  base_agi REAL,
  base_int REAL,
  str_gain REAL,
  agi_gain REAL,
  int_gain REAL,
  attack_range REAL,
  projectile_speed REAL,
  attack_rate REAL,
  move_speed REAL,
  turn_rate REAL,
  cm_enabled REAL,
  legs REAL,
  pro_ban REAL,
  pro_win REAL,
  pro_pick REAL,
  pick_1 REAL,
  win_1 REAL,
  pick_2 REAL,
  win_2 REAL,
  pick_3 REAL,
  win_3 REAL,
  pick_4 REAL,
  win_4 REAL,
  pick_5 REAL,
  win_5 REAL,
  pick_6 REAL,
  win_6 REAL,
  pick_7 REAL,
  win_7 REAL,
  pick_8 REAL,
  win_8 REAL,
  null_pick REAL,
  PRIMARY KEY (id)
);
