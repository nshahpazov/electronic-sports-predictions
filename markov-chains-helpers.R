get_bins <- function (df, nbin = 20, feature = "gold_difference") {
  df %>%
    select(contains(feature)) %>%
    as.matrix() %>%
    c() %>%
    quantile(na.rm = TRUE, probs = seq(0, 1, 1 / nbin))
}

as_binned_matrix <- function (df, nbin = 20, feature = "gold_difference") {
  bins <- get_bins(df, nbin, feature)
  df %>%
    select(contains(feature)) %>%
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

acc <- function (test_set, tsbm, winners, losers, t) {
  d_win <- get_trajectory_probability(tsbm, winners, t = t, window = 5)
  d_los <- get_trajectory_probability(tsbm, losers, t = t, window = 5)
  
  mean(0 + ((d_win > d_los) == as.logical(test_set$radiant_win)), na.rm = TRUE)
}

mc_accuracy <- function (test_set, tsbm, winners, losers, t) {
  d_win <- get_trajectory_probability(tsbm, winners, t = t, window = 5)
  d_los <- get_trajectory_probability(tsbm, losers, t = t, window = 5)
  
  pred_win <- d_win > d_los
  
  pred_win == as.logical(test_set$radiant_win) %>%
    as.numeric() %>%
    mean(na.rm = TRUE)
}

pca_transform <- function (data, range = 0:99, cols = WINDOW_COLS[-2]) {
  range %>%
    map(~cols_window(. + 1:1, cols = cols)) %>%
    map(~as.formula(paste("~", paste(., collapse = "+")))) %>%
    map(
      ~ princomp(
        .x,
        data = data,
        na.action = na.omit,
        center = TRUE,
        scale = TRUE
      ) %>%
        predict(newdata = data) %>%
        .[, 1]
    ) %>%
    {names(.) <- imap(range + 1, ~glue("pca_{.y}")); .} %>%
    as.data.frame()
}

reflect <- function (df, winners = FALSE) {
  df %>%
    filter(as.logical(radiant_win) == reflect_winners) %>%
    mutate_at(vars(matches("difference")), ~ifelse(is.na(.), ., . * -1)) %>%
    mutate(radiant_win = as.factor(TRUE)) %>%
    bind_rows(filter(df, as.logical(radiant_win) != reflect_winners))
}