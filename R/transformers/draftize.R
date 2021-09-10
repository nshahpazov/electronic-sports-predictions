#' Takes a players dataframe and returns the 226-dimensional dataframe having ith index 1 if the 
#' ith hero is present in radiant and i+112'th index being 1 if ith hero is present in the dire team
#' @param players A dataframe with information about players on each match
#' @return A dataframe with the draft indicators.
draftize <- function(players) {
  players %>%
    mutate(hero_id = ifelse(player_slot > 5, hero_id + 113, hero_id)) %>%
      mutate(val = 1) %>%
      pivot_wider(
        names_from = "hero_id",
        values_from = "val",
        values_fill = 0,
        names_glue = "hero_{hero_id}"
      ) %>%
      select(match_id, starts_with("hero")) %>%
      select(-hero_damage, -hero_healing) %>%
      group_by(match_id) %>%
      summarise(across(everything(), ~sum(.x, na.rm = TRUE)))
}