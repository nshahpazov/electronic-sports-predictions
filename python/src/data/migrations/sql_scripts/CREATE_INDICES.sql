CREATE INDEX match_index ON match(match_id);
CREATE INDEX match_account_index ON match_player(match_id, account_id, hero_id);
CREATE INDEX player_index ON player(account_id);
CREATE INDEX player_match_rating_index ON player_match_rating(match_id, account_id);
CREATE INDEX player_match_rating_index_v2 ON player_match_rating_v2(match_id, account_id);
CREATE INDEX player_heroes_ranking_index ON player_heroes_ranking(account_id, hero_id);
CREATE INDEX player_hero_win_rate_index ON player_hero_win_rate(account_id, hero_id);
