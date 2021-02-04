generate_ratios_df <- function (team_heroes_df) {
  winners_hero_freq_df <- team_heroes_df %>%
    group_by(account_id) %>%
    filter(radiant_win) %>%
    generate_combinations() %>%
    ungroup()

  losers_hero_freq_df <- team_heroes_df %>%
    filter(!radiant_win) %>%
    group_by(account_id) %>%
    generate_combinations() %>%
    ungroup()

  winners_hero_freq_df %>%
    mutate(ratio = n / losers_hero_freq_df$n) %>%
    select(-n)
}

generate_combinations <- function (hero_matches_df) {
  crossing(hero_id_team_1 = 0:112, hero_id_team_2 = 0:112)  %>%
    filter(hero_id_team_1 != hero_id_team_2) %>%
    left_join(count(hero_matches_df, hero_id_team_1, hero_id_team_2)) %>%
    mutate(n = replace_na(n, 1))
}

generate_team_heroes_df <- function (players_df) {
  players_df %>%
    left_join(select(matches_df, match_id, radiant_win), by = "match_id") %>%
    mutate(team = ifelse(player_slot < 6, "team_1", "team_2")) %>%
    select(match_id, team, hero_id, radiant_win, account_id) %>%
    pivot_wider(
      id_cols = match_id,
      names_from = team,
      values_from = c(hero_id, account_id, radiant_win)
    ) %>%
    unchop(everything()) %>%
    select(-radiant_win_team_2) %>%
    rename(radiant_win = radiant_win_team_1, account_id = account_id_team_1)
}
