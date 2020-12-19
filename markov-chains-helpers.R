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

as_binned_matrix <- function (df, nbin = 20) {
  bins <- get_bins(df, nbin)
  df %>%
    select(contains("gold")) %>%
    mutate_all(~cut(., breaks = bins, labels = 1:nbin)) %>%
    data.matrix()
}

construct_transition_matrix <- function (m, nbin = 20, time = 60) {
  freq <- matrix(0, nbin, nbin)

  for (i in 1:time) {
    msk <- !is.na(m[, i + 1])
    idx <- cbind(m[msk, i], m[msk, i + 1])
    freq[idx] <- freq[idx] + 1
  }
  freq
}
