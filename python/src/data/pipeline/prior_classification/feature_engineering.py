import pandas as pd

def aggr(df: pd.DataFrame, variable: str, agg: callable):
    columns_team_1 = [f"{variable}_t_{i}" for i in range(5)]
    columns_team_2 = [f"{variable}_t_{128 + i}" for i in range(5)]
    return agg(df[columns_team_1]) - agg(df[columns_team_2])


def generate_player_time_features(player_time_df: pd.DataFrame):
    aggregations = [
        ("q1", lambda df: df.quantile(0.25, axis=1)),
        ("q3", lambda df: df.quantile(0.75, axis=1)),
        ("median", lambda df: df.median(axis=1)),
        ("mean", lambda df: df.mean(axis=1)),
    ]
    variables = ["xp", "lh", "gold"]
    df = player_time_df.copy().assign(times=lambda df: (df.times / 60).astype(int))

    columns_to_drop = df.columns[df.columns.str.contains("_t_")]
    aggregated_df = df.assign(**{
        f"{var}_{agg}_diff": aggr(df, var, fn) for var in variables for agg, fn in aggregations
    }).drop(columns=columns_to_drop)

    return aggregated_df

if __name__ == "__main__":
    matches_df = pd.read_csv("../datasets/raw/match.csv")
    player_ratings_df = pd.read_csv("../datasets/raw/player_ratings.csv")
    player_time_df = pd.read_csv("../datasets/raw/player_time.csv")
    ability_upgrades_df = pd.read_csv("../datasets/raw/ability_upgrades.csv")
    generate_player_time_features(player_time_df)
