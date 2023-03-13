SELECT
-- has roles indicators in team 1
-- SELECT roles like "%Carry%" as has_carry from hero_characteristics;
{% if has_roles %}
  sum(hc.roles like "%Carry%" and player_slot < 128) as has_carry_1,
  sum(hc.roles like "%Escape%" and player_slot < 128) as has_escape_1,
  sum(hc.roles like "%Nuker%" and player_slot < 128) as has_nuker_1,
  sum(hc.roles like "%Initiator%" and player_slot < 128) as has_initiator_1,
  sum(hc.roles like "%Durable%" and player_slot < 128) as has_durable_1,
  sum(hc.roles like "%Disabler%" and player_slot < 128) as has_disabler_1,
  sum(hc.roles like "%Support%" and player_slot < 128) as has_support_1,
  sum(hc.roles like "%Pusher%" and player_slot < 128) as has_pusher_1,
  sum(hc.roles like "%Jungler%" and player_slot < 128) as has_jungler_1,

  -- has roles indicators in team 2
  sum(hc.roles like "%Carry%" and player_slot >= 128) as has_carry_2,
  sum(hc.roles like "%Escape%" and player_slot >= 128) as has_escape_2,
  sum(hc.roles like "%Nuker%" and player_slot >= 128) as has_nuker_2,
  sum(hc.roles like "%Initiator%" and player_slot >= 128) as has_initiator_2,
  sum(hc.roles like "%Durable%" and player_slot >= 128) as has_durable_2,
  sum(hc.roles like "%Disabler%" and player_slot >= 128) as has_disabler_2,
  sum(hc.roles like "%Jungler%" and player_slot >= 128) as has_jungler_2,
  sum(hc.roles like "%Support%" and player_slot >= 128) as has_support_2,
  sum(hc.roles like "%Pusher%" and player_slot >= 128) as has_pusher_2,

  -- number primary attributes in each the radiant team
  sum(hc.primary_attr like "%agi%" and player_slot < 128) as has_primary_agi_1,
  sum(hc.primary_attr like "%int%" and player_slot < 128) as has_primary_int_1,
  sum(hc.primary_attr like "%str%" and player_slot < 128) as has_primary_str_1,

  -- number primary attributes in each the dire team
  sum(hc.primary_attr like "%agi%" and player_slot >= 128) as has_primary_agi_2,
  sum(hc.primary_attr like "%int%" and player_slot >= 128) as has_primary_int_2,
  sum(hc.primary_attr like "%str%" and player_slot >= 128) as has_primary_str_2,

  -- number of attack types being Melee or Ranged in team 1 (Radiant)
  sum(hc.attack_type like "%Melee%" and player_slot < 128) as has_melee_1,
  sum(hc.attack_type like "%Ranged%" and player_slot < 128) as has_ranged_1,

  -- number of attack types being Melee or Ranged in team 2 (Dire)
  sum(hc.attack_type like "%Melee%" and player_slot >= 128) as has_melee_2,
  sum(hc.attack_type like "%Ranged%" and player_slot >= 128) as has_ranged_2,
{% endif %}

-- average difference between the two teams of hero numeric characteristics
{% if has_hero_characteristics %}
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.base_attack_min ELSE -hc.base_attack_min END), 0) AS "base_attack_min_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.base_attack_max ELSE -hc.base_attack_max END), 0) AS "base_attack_max_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.base_armor ELSE -hc.base_armor END), 0) AS "base_armor_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.base_str ELSE -hc.base_str END), 0) AS "base_str_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.base_agi ELSE -hc.base_agi END), 0) AS "base_agi_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.base_int ELSE -hc.base_int END), 0) AS "base_int_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.str_gain ELSE -hc.str_gain END), 0) AS "str_gain_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.agi_gain ELSE -hc.agi_gain END), 0) AS "agi_gain_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.int_gain ELSE -hc.int_gain END), 0) AS "int_gain_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.attack_range ELSE -hc.attack_range END), 0) AS "attack_range_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.projectile_speed ELSE -hc.projectile_speed END), 0) AS "projectile_speed_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.attack_rate ELSE -hc.attack_rate END), 0) AS "attack_rate_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.move_speed ELSE -hc.move_speed END), 0) AS "move_speed_diff",
  coalesce(AVG(CASE WHEN player_slot < 128 THEN hc.turn_rate ELSE -hc.turn_rate END), 0) AS "turn_rate_diff",
{% endif %}

-- indicators of played heroes, also known as the draft of the game
{%- if has_played_heroes -%}
  -- hero_{j} = I(hero_j belongs to radiant team)
  {%- for i in range(1, 113) %}
    SUM(mp.hero_id = {{i}} and mp.player_slot < 128) AS "hero_{{i}}",
  {%- endfor %}
  -- hero_{j+112} = I(hero_j belongs to dire team)
  {%- for i in range(1, 113) %}
    SUM(mp.hero_id = {{i}} and mp.player_slot >= 128) AS "hero_{{112 + i}}",
  {%- endfor %}
{%- endif -%}

-- mmr ratings
-- try with separate for now
{%- if has_mmr_ratings -%}
  (CASE WHEN player_slot = 0 then p.mmr_estimate END) player_1_mmr,
  (CASE WHEN player_slot = 1 then p.mmr_estimate END) player_2_mmr,
  (CASE WHEN player_slot = 2 then p.mmr_estimate END) player_3_mmr,
  (CASE WHEN player_slot = 3 then p.mmr_estimate END) player_4_mmr,
  (CASE WHEN player_slot = 4 then p.mmr_estimate END) player_5_mmr,
  (CASE WHEN player_slot = 5 then p.mmr_estimate END) player_6_mmr,
  (CASE WHEN player_slot = 6 then p.mmr_estimate END) player_7_mmr,
  (CASE WHEN player_slot = 7 then p.mmr_estimate END) player_8_mmr,
  (CASE WHEN player_slot = 8 then p.mmr_estimate END) player_9_mmr,
  (CASE WHEN player_slot = 9 then p.mmr_estimate END) player_10_mmr,
{%- endif -%}

-- unique match id
mp.match_id,

-- response target variable
m.radiant_win,

-- start time (it's important for the splitting o f train\test sets)
m.start_time

FROM match m
LEFT JOIN match_player mp
ON m.match_id = mp.match_id
LEFT JOIN player p
ON mp.account_id = p.account_id
LEFT JOIN hero_characteristics hc
ON hc.hero_id = mp.hero_id
GROUP BY m.match_id
HAVING SUM(MP.leaver_status) = 0
ORDER BY m.start_time
{% if limit %}
  LIMIT {{limit}}
{% endif %};
