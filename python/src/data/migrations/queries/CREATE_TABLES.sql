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
  hero_id INTEGER,
  gold INTEGER,
  deaths INTEGER,
  hero_damage INTEGER,
  scaled_hero_damage INTEGER,
  last_hits INTEGER,
  denies INTEGER,
  scaled_hero_healing INTEGER,
  tower_damage INTEGER,
  xp_per_min INTEGER,
  kills INTEGER,
  scaled_tower_damage INTEGER,
  hero_healing INTEGER,
  assists INTEGER,
  gold_per_min INTEGER,
  level INTEGER,
  PRIMARY KEY (id)
);
