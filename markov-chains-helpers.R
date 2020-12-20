get_bins <- function (df, nbin = 20) {
  max_gold <- df %>%
    select(contains("gold_difference")) %>%
    max(na.rm = TRUE) %>%
    max(na.rm = TRUE)

  min_gold <- df %>%
    select(contains("gold_difference")) %>%
    min(na.rm = TRUE) %>%
    min(na.rm = TRUE)

  bins <- seq(min_gold, max_gold, length.out = nbin + 1)
}

as_binned_matrix <- function (df, nbin = 20, field = "gold") {
  df %>%
    select(contains(field)) %>%
    mutate_all(~cut(., breaks = get_bins(df, nbin), labels = 1:nbin)) %>%
    data.matrix(rownames.force = TRUE)
}

construct_transition_matrix <- function (m, nbin = 20, time = 80) {
  freq <- matrix(0, nbin, nbin)
  t <- rowSums(0 + !is.na(m))
  for (i in 1:nrow(m)) {
    for (j in 1:min(t[i], time) - 1) {
      freq[m[i, j], m[i, j + 1]] <- freq[m[i, j], m[i, j + 1]]  + 1
    }
  }
  
  freq / rowSums(freq)
}

reflect_losers <- function (df) {
  df %>%
    filter(!as.logical(radiant_win)) %>%
    mutate_at(vars(matches("difference")), ~ifelse(is.na(.), ., . * -1)) %>%
    mutate(radiant_win = as.factor(TRUE)) %>%
    bind_rows(filter(df, as.logical(radiant_win)))
}