import os
from pymongo import MongoClient
from progress.bar import Bar
from six.moves import cPickle
import numpy as np
from sklearn import preprocessing

num_heroes = 113

def save_as_pk(data, filename):
    fout = open(filename, 'wb')
    cPickle.dump(data, fout, protocol=cPickle.HIGHEST_PROTOCOL)
    fout.close()

if __name__ == '__main__':
	client = MongoClient()
	db = client['701']
	player = db['player']
	N = player.count()
	print('Scanning through ' + str(N) + ' players in collection "player"...')

	hero_player_winrate = {}
	for hero_id in range(1, num_heroes+1):
		hero_player_winrate[str(hero_id)] = {}
		hero_player_winrate[str(hero_id)]['unknown player'] = 0.5

    # iterates over all players
    # might not need
	for i, m in enumerate(player.find()):
        # takes the id of the current player
		player_id = str(m['account_id'])
		for hero in m['heroes']:
			if hero['games'] > 10:
				hero_player_winrate[hero['hero_id']][player_id] = float(hero['win']) / hero['games']
			else:
				hero_player_winrate[hero['hero_id']][player_id] = 0.5

	cnt = 0
	X = np.zeros(num_heroes * (N + 1)) + 0.5
	for hero_id in hero_player_winrate.keys():
		for player_id in hero_player_winrate[hero_id].keys():
			X[cnt] = hero_player_winrate[hero_id][player_id]
			cnt += 1

    # here X is used just for the sake of scaling (why ?!?!!?!???!? O.o)
	min_max_scaler = preprocessing.MinMaxScaler()
	X_scaled = min_max_scaler.fit_transform(X)

	cnt = 0
	for hero_id in hero_player_winrate.keys():
		for player_id in hero_player_winrate[hero_id].keys():
			hero_player_winrate[hero_id][player_id] = X_scaled[cnt]
			cnt += 1

	print(hero_player_winrate['1'])
	save_as_pk(hero_player_winrate, 'hero_player_winrate.pk')


	"""
	y = []
	x = []
	bar = Bar('Processing', max=N)
	for i, m in enumerate(matches.find()):
		bar.next()
		a,b = get_match_detail(m)
		if a==-1:
			continue
		y.append(a)
		x.append(b)
	bar.finish()
	X = np.array(x) # features
	Y = np.array(y) # label
	"""
