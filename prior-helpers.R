generate_combinations <- function (hero_matches_df) {
  crossing(hero_team_1 = 0:112, hero_team_2 = 0:112)  %>%
    filter(hero_team_1 != hero_team_2) %>%
    left_join(., count(hero_matches_df, hero_team_1, hero_team_2)) %>%
    mutate(n = replace_na(n, 1))
}

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
