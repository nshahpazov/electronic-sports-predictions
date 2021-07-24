get_bins <- function (df, nbin = 20, feature = "gold_difference", minutes = 1:ncol(df)) {
  x <- df %>%
    select(contains(feature)) %>%
    .[, minutes] %>%
    as.matrix() %>%
    c() %>%
    quantile(na.rm = TRUE, probs = seq(0, 1, 1 / nbin))
}

as_binned_matrix <- function (df, nbin = 20, feature = "gold_difference", minutes = 1:ncol(df)) {
  df %>%
    select(contains(feature)) %>%
    mutate_all(~cut(., breaks = get_bins(df, nbin, feature, minutes), labels = 1:nbin)) %>%
    data.matrix(rownames.force = TRUE)
}

construct_transition_matrix <- function (games, nbin = 20, time = 100) {
  # TODO: check that!
  tm <- matrix(0, nbin, nbin)
  t <- rowSums(0 + !is.na(games))

  for (i in 1:nrow(games)) {
    for (j in 1:min(t[i], time) - 1) {
      tm[games[i, j], games[i, j + 1]] <- tm[games[i, j], games[i, j + 1]]  + 1
    }
  }
  
  tm / rowSums(tm)
}

# tm = transition matrix, bm = bin matrix
get_trajectory_probability <- function(bin_matrix, transition_matrix, t = 6, window = 5) {
  probs <- c()
  # browser()
  for (i in 1:nrow(bin_matrix)) {
    prob <- 1
    for (j in (t - window - 1):t) {
      # take the probability of moving from bin_matrix[]
      current <- transition_matrix[bin_matrix[i, j], bin_matrix[i , j + 1]]
      prob <- prob * ifelse(is.na(current), 1, current)
    }
    # I'm multiplying the probabilities
    probs[i] <- prob
  }
  probs
}

get_mc_accuracy <- function (test_set, tsbm, winners, losers, t) {
  d_win <- get_trajectory_probability(tsbm, winners, t = t, window = 5)
  d_loss <- get_trajectory_probability(tsbm, losers, t = t, window = 5)

  predicted <- d_win > d_loss
  actual <- as.logical(test_set$radiant_win)

  mean((predicted == actual), na.rm = TRUE)
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