diff_means <- function (tbl, rgx_1, rgx_2) {
  rowMeans(select(tbl, matches(rgx_1))) - rowMeans(select(tbl, matches(rgx_2)))
}

cols_window <- function (window, cols = WINDOW_COLS) {
  cols %>%
    map(~paste(., window, sep = "_")) %>%
    reduce(c)
}

feat_formula <- function (window, cols = WINDOW_COLS, outcome = "radiant_win") {
  cols_window(window, cols) %>%
    map(~as.formula(paste(outcome, "~", paste(., collapse = "+"))))
}

standardize_time_df <- function (data) {
  data %>%
    recipe(radiant_win ~ .) %>% 
    step_center(-match_id, -radiant_win) %>%
    step_scale(-match_id, -radiant_win) %>%
    prep() %>%
    juice()
}

train_lr <- function (data, control, interval = 0:95, window_length = 5, cols = WINDOW_COLS) {
  interval %>%
    map(~cols_window(. + (1:window_length), cols)) %>%
    map(~as.formula(paste("radiant_win ~ ", paste(., collapse = "+")))) %>%
    map(
      ~train(
        form = .,
        data = data,
        trControl = control,
        method = "glm",
        na.action = na.pass,
        family = "binomial",
        metric = "Accuracy"
      )
    )
}

train_dt <- function (data, control, interval = 1:95, window_length = 5, cols = WINDOW_COLS) {
  interval %>%
    map(~cols_window(. + (1:window_length), cols)) %>%
    map(~as.formula(paste("radiant_win~", paste(., collapse = "+")))) %>%
    map(
      ~train(
        form = .,
        data = data,
        trControl = control,
        method = "glm",
        na.action = na.pass,
        family = "binomial",
        metric = "Accuracy"
      )
    )
}

get_test_accuracies <- function (model, data, cols = WINDOW_COLS, t = 40) {
  columns <- imap(6:t, ~cols_window(. - seq(6, 2, by = -1), ))
  predictions <- imap(columns, ~predict(model[.y], newdata = data[, .])[[1]])

  columns %>%
    imap(~c("radiant_win", columns[[.y]])) %>%
    imap(~accuracy(predictions[[.y]], drop_na(data[, .])$radiant_win)) %>%
    unlist()
}

matrix_to_df <- function (m, cols = c("col", "row", "value")) {
  m %>%
    reshape::melt() %>%
    na.omit() %>%
    .[order(.$X1), ] %>%
    { colnames(.) <- cols; . }
}
