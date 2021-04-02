SELECT mp.match_id, mp.account_id, mp.hero_id, mp.player_slot, m.radiant_win,
	   hs.xp_per_min, hs.kills_per_min, hs.hero_damage_per_min, hs.last_hits_per_min,
	   hs.hero_healing_per_min, hs.tower_damage, hs.gold_per_min,
CASE
-- used for the matching between mmr_distribution.percentile and hero stats
WHEN md.percentile >= 0.95 THEN 0.95
WHEN md.percentile >= 0.9 THEN 0.9
WHEN md.percentile >= 0.8 THEN 0.8
WHEN md.percentile >= 0.7 THEN 0.7
WHEN md.percentile >= 0.6 THEN 0.6
WHEN md.percentile >= 0.5 THEN 0.5
WHEN md.percentile >= 0.4 THEN 0.4
WHEN md.percentile >= 0.3 THEN 0.3
WHEN md.percentile >= 0.2 THEN 0.2
-- impute with the median for not found
WHEN md.percentile IS NULL THEN 0.5
ELSE 0.1
END AS floored_percentile
FROM match_player AS mp
LEFT JOIN match AS m
ON mp.match_id  = m.match_id
-- the player table is used for extracting the mmr_estimate
LEFT JOIN player p
ON p.account_id = mp.account_id
LEFT JOIN mmr_distribution md
ON md.bin_name = (SELECT bin_name
                  FROM mmr_distribution md2
                  WHERE p.mmr_estimate >= md2.bin_name
                  ORDER BY bin_name DESC
                  LIMIT 1
                )
LEFT JOIN hero_stats hs
ON mp.hero_id = hs.hero_id and floored_percentile = hs.percentile;