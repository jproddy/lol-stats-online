import pandas as pd
import time
from tqdm import tqdm

from riotwatcher import LolWatcher, ApiError
from .api_key import API_KEY

REGION = 'na1'

def get_account_id(account_name):
	watcher = LolWatcher(API_KEY)
	account = watcher.summoner.by_name(REGION, account_name)
	return account['accountId']

def get_matchlist(account_id, region=REGION):
	''' retrieves list of all matches for the given account id and returns as a dataframe '''
	watcher = LolWatcher(API_KEY)
	matches = []
	i = 0
	# queue ids limit the games to 5v5 sr (norms, draft, flex, soloq, clash)
	valid_queue_ids = [400, 420, 430, 440, 700]

	print('fetching matchlist:')
	pbar = tqdm(total=float('inf'), mininterval=0.1)
	while True:
		try:
			match = watcher.match.matchlist_by_account(
				region,
				account_id,
				queue=valid_queue_ids,
				begin_index=100*i
			)
			if match['matches']:
				matches.append(match)
				i += 1
				time.sleep(.1)
				pbar.update(len(match['matches']))
			else:
				break
		except:
			pass

	all_matches = [m for match in matches for m in match['matches']]
	pbar.total = len(all_matches)
	pbar.close()

	df = pd.DataFrame(all_matches)
	df.rename({'timestamp':'creation', 'gameId': 'game_id'}, axis=1, inplace=True)
	df.set_index('game_id', drop=False, inplace=True)
	df.drop(['season', 'role', 'lane', 'platformId', 'champion'], axis=1, inplace=True)
	return df

def get_timelines(game_ids, region=REGION):
	''' retrieves detailed reports of all match timelines in the given matchlist and returns as a dataframe '''
	watcher = LolWatcher(API_KEY)
	timelines = []
	game_ids_success = []
	failed = []

	print('fetching timelines:')
	for i, game_id in enumerate(tqdm(game_ids)):
		for _ in range(3):
			try:
				timelines.append(watcher.match.timeline_by_match(region, game_id))
				game_ids_success.append(game_id)
				break
			except:
				time.sleep(1.5)
		else:
			failed.append(game_id)
		time.sleep(1.5)
	if failed:
		print('game ids failed:', failed)

	df_tl = pd.DataFrame(timelines, index=game_ids_success)
	df_tl.index.rename('game_id', inplace=True)
	df_tl.sort_index(inplace=True)
	return df_tl

def get_forfeits(df, region=REGION):
	'''return a series containing if each game in df was forfeit or finished normally'''
	df_tl = get_timelines(df.game_id, region)
	df_tl['winner'] = df.winner
	return df_tl.apply(lambda x: extract_forfeit_from_frames(x.frames, x.winner), axis=1)

def extract_forfeit_from_frames(frames, winner):
	'''uses timeline frames to determine if a given game was forfeit or finished normally'''
	nexus_turrets = {1748: False, 2177: False, 12611: False, 13052: False}
	for frame in frames:
		for event in frame['events']:
			if event['type'] == 'BUILDING_KILL' and event['towerType'] == 'NEXUS_TURRET':
				nexus_turrets[event['position']['x']] = True
	blue_nexus_turrets_destroyed = nexus_turrets[1748] and nexus_turrets[2177]
	red_nexus_turrets_destroyed = nexus_turrets[12611] and nexus_turrets[13052]
	forfeit = not ((red_nexus_turrets_destroyed & (winner == 100)) | (blue_nexus_turrets_destroyed & (winner == 200)))
	return int(forfeit)

def get_matches(df, region=REGION):
	'''collects games from riot api'''
	watcher = LolWatcher(API_KEY)
	matches = []
	game_ids_success = []
	failed = []

	print('fetching matches:')
	for i, game_id in enumerate(tqdm(df.game_id)):
		for _ in range(3):
			try:
				matches.append(watcher.match.by_id(region, game_id))
				game_ids_success.append(game_id)
				break
			except:
				time.sleep(1.5)
		else:
			failed.append(game_id)
		time.sleep(1.5)
	if failed:
		print('game ids failed:', failed)

	df_m = pd.DataFrame(matches)
	df_m.rename(columns={'gameId': 'game_id'}, inplace=True)
	df_m.set_index('game_id', drop=False, inplace=True)
	return df_m

def filter_remakes(df):
	'''returns tuple (full-length games, remakes). cutoff set to 300 s'''
	if 'duration' in df.columns:
		remake_mask = df.duration > 300
	elif 'gameDuration' in df.columns:
		remake_mask = df.gameDuration > 300
	return df[remake_mask], df[~remake_mask]
