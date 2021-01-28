generate_ratios_df <- function (team_heroes_df) {
  winners_hero_freq_df <- team_heroes_df %>%
    filter(radiant_win) %>%
    generate_combinations()

  losers_hero_freq_df <- team_heroes_df %>%
    filter(!radiant_win) %>%
    generate_combinations()
  
  winners_hero_freq_df %>%
    mutate(ratio = n / losers_hero_freq_df$n) %>%
    select(-n)
}

generate_team_heroes_df <- function (players_df) {
  players_df %>%
    left_join(select(matches_df, match_id, radiant_win), by = "match_id") %>%
    mutate(team = ifelse(player_slot < 6, "hero_team_1", "hero_team_2")) %>%
    select(match_id, team, hero_id, radiant_win) %>%
    pivot_wider(names_from = team, values_from = hero_id) %>%
    unchop(everything())
}

generate_combinations <- function (hero_matches_df) {
  crossing(hero_team_1 = 0:112, hero_team_2 = 0:112)  %>%
    filter(hero_team_1 != hero_team_2) %>%
    left_join(count(hero_matches_df, hero_team_1, hero_team_2)) %>%
    mutate(n = replace_na(n, 1))
}