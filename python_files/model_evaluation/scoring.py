def make_rps(df, agency='None'):

    if agency == 'B365':

        # extract columns H, D, and A and convert to a NumPy array
        pred_probs = df[['B365H', 'B365D', 'B365A']].values

        # create a dictionary mapping each label to its one-hot encoding
        label_map = {'H': [1, 0, 0], 'D': [0, 1, 0], 'A': [0, 0, 1]}

        # use NumPy's where function to create an array of one-hot encoded labels
        label_list = []
        for val in df['FTR']:
            label_list.append(label_map[val])
        obs_outcomes = np.array(label_list)

        # compute the RPS
        rps_list = []
        for i in range(pred_probs.shape[0]):
            rps_list.append(0.5 * ((pred_probs[i][0]-obs_outcomes[i][0])**2+(pred_probs[i][0]-obs_outcomes[i][0]+pred_probs[i][1]-obs_outcomes[i][1])**2))

        print('The RPS score for this model is: ')
        return np.average(rps_list)

    elif agency == 'PS':

        # extract columns H, D, and A and convert to a NumPy array
        pred_probs = df[['PSH', 'PSD', 'PSA']].values

        # create a dictionary mapping each label to its one-hot encoding
        label_map = {'H': [1, 0, 0], 'D': [0, 1, 0], 'A': [0, 0, 1]}

        # use NumPy's where function to create an array of one-hot encoded labels
        label_list = []
        for val in df['FTR']:
            label_list.append(label_map[val])
        obs_outcomes = np.array(label_list)

        # compute the RPS
        rps_list = []
        for i in range(pred_probs.shape[0]):
            rps_list.append(0.5 * ((pred_probs[i][0]-obs_outcomes[i][0])**2+(pred_probs[i][0]-obs_outcomes[i][0]+pred_probs[i][1]-obs_outcomes[i][1])**2))

        print('The RPS score for this model is: ')
        return np.average(rps_list)

    else:

        # extract columns H, D, and A and convert to a NumPy array
        pred_probs = df[['home_win', 'draw', 'away_win']].values

        # create a dictionary mapping each label to its one-hot encoding
        label_map = {0: [1, 0, 0], 1: [0, 1, 0], 2: [0, 0, 1]}

        # use NumPy's where function to create an array of one-hot encoded labels
        label_list = []
        for val in df['outcome']:
            label_list.append(label_map[val])
        obs_outcomes = np.array(label_list)

        # compute the RPS
        rps_list = []
        for i in range(pred_probs.shape[0]):
            rps_list.append(0.5 * ((pred_probs[i][0]-obs_outcomes[i][0])**2+(pred_probs[i][0]-obs_outcomes[i][0]+pred_probs[i][1]-obs_outcomes[i][1])**2))

        print('The RPS score for this model is: ')
        return np.average(rps_list)
