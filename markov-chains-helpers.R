get_bins <- function (df, nbin = 20) {
  df %>%
    select(contains("gold_difference")) %>%
    as.matrix() %>%
    c() %>%
    quantile(na.rm = TRUE, probs = seq(0, 1, 1 / nbin))
}

as_binned_matrix <- function (df, nbin = 20, field = "gold") {
  bins <- get_bins(df, nbin)
  df %>%
    select(contains(field)) %>%
    mutate_all(~cut(., breaks = bins, labels = 1:nbin)) %>%
    data.matrix(rownames.force = TRUE)
}

construct_transition_matrix <- function (games, nbin = 20, time = 100) {
  tm <- matrix(0, nbin, nbin)
  t <- rowSums(0 + !is.na(games))

  for (i in 1:nrow(games)) {
    for (j in 1:min(t[i], time) - 1) {
      tm[games[i, j], games[i, j + 1]] <- tm[games[i, j], games[i, j + 1]]  + 1
    }
  }
  
  tm / rowSums(tm)
}

get_trajectory_probability <- function (bm, tm, t = 1, window = 5) {
  probs <- c()
  for (i in 1:nrow(bm)) {
    prob <- 1
    for (j in t:t + window - 1) {
      current <- tm[bm[i, j], bm[i , j + 1]]
      prob <- prob * ifelse(is.na(current), 1, current)
    }
    probs[i] <- prob
  }
  probs
}

mc_accuracy <- function (tsbm, winners, losers, t) {
  d_win <- get_trajectory_probability(tsbm, winners, t = t, window = 5)
  d_los <- get_trajectory_probability(tsbm, losers, t = t, window = 5)
  
  pred_win <- d_win > d_los
  
  pred_win == as.logical(test_set$radiant_win) %>%
    as.numeric() %>%
    mean(na.rm = TRUE)
}

reflect <- function (df, reflect_winners = FALSE) {
  df %>%
    filter(as.logical(radiant_win) == reflect_winners) %>%
    mutate_at(vars(matches("difference")), ~ifelse(is.na(.), ., . * -1)) %>%
    mutate(radiant_win = as.factor(TRUE)) %>%
    bind_rows(filter(df, as.logical(radiant_win) != reflect_winners))
}