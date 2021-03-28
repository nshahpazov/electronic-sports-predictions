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
