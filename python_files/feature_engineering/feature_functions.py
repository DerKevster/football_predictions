from python_files.feature_engineering.baseline_footballdata_merge_df import make_merged_df

df = make_merged_df()

def make_past_rounds_df(round_, df, past_rounds):
    prev_round_df = df.loc[df['round'] == round_-1]
    past_rounds_df = pd.DataFrame()

    if round_ - past_rounds > 0:
        if past_rounds == 1:
            return prev_round_df
        else:
            for i in range(past_rounds):
                next_past_rounds_df = df.loc[df['round'] == round_-1-i]
                if i == 0:
                    past_rounds_df = prev_round_df
                else:
                    past_rounds_df = pd.concat([past_rounds_df, next_past_rounds_df], axis=0)
    else:
        print("Error: The past rounds you are asking for do not exist")
    return past_rounds_df

def get_goals(team, round, df, past_rounds):
    past_rounds_df = make_past_rounds_df(round, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['home_club_goals']
        elif current_game['away_team'] == team:
            goals += current_game['away_club_goals']
        #print(current_game)
    return goals

def get_conc(team, round, df, past_rounds):
    past_rounds_df = make_past_rounds_df(round, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['away_club_goals']
        elif current_game['away_team'] == team:
            goals += current_game['home_club_goals']
    return goals

def get_corner(team, round, df, past_rounds):
    past_rounds_df = make_past_rounds_df(round, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HC']
        elif current_game['away_team'] == team:
            goals += current_game['AC']
    return goals

def get_shots(team, round, df, past_rounds):
    past_rounds_df = make_past_rounds_df(round, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HS']
        elif current_game['away_team'] == team:
            goals += current_game['AS']
    return goals

def get_targets(team, round, df, past_rounds):
    past_rounds_df = make_past_rounds_df(round, df, past_rounds)
    goals = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goals += current_game['HST']
        elif current_game['away_team'] == team:
            goals += current_game['AST']
    return goals

def get_goal_diff(team, round, df):
    past_rounds_df = make_past_rounds_df(round, df, (round-1))
    goal_diff = 0
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            goal_diff += (current_game['home_club_goals'] - current_game['away_club_goals'])
        elif current_game['away_team'] == team:
            goal_diff += (current_game['away_club_goals'] - current_game['home_club_goals'])
        #print(current_game)
    return goal_diff

def get_opp_avg(team, round, df):
    past_rounds_df = make_past_rounds_df(round, df, past_rounds)

    oppos = []
    for i in range(len(past_rounds_df)):
        current_game = past_rounds_df.iloc[i, :]
        if current_game['HomeTeam'] == team:
            oppos.append(current_game['away_team'])
        elif current_game['away_team'] == team:
            oppos.append(current_game['HomeTeam'])

    oppos_goaldiff = [get_goal_diff(oppo, round, df) for oppo in oppos]
    return oppos_goaldiff.mean()
