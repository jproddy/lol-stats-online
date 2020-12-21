from flask import session
from flask import current_app as app

import sqlite3
import pandas as pd
import numpy as np

from lol_online.db import get_db
from . import riot_api, aggregate_stats


def generate_player_stats(account_name, internal_db_only=True):
	'''calculates player statistics for api class PlayerStats'''
	account_id = riot_api.get_account_id(account_name)

	df_player_games, df_other_players = internal_generate_dataframes(account_id)
	if not internal_db_only:
		df_player_games, df_other_players = external_generate_dataframes(account_id, df_player_games, df_other_players)

	oldest = aggregate_stats.oldest_game(df_player_games)
	newest = aggregate_stats.newest_game(df_player_games)
	df_ally, df_enemy = aggregate_stats.players_by_team(account_id, df_player_games, df_other_players)
	df_player_champion_winrates = aggregate_stats.winrate_by_champ(df_player_games)
	df_ally_champion_winrates = aggregate_stats.winrate_by_champ(df_ally)
	df_enemy_champion_winrates = aggregate_stats.winrate_by_champ(df_enemy)
	df_blue_red_winrate = aggregate_stats.blue_red_winrate(df_player_games)
	df_game_durations = aggregate_stats.average_game_durations(df_player_games)
	image_game_durations_plot = aggregate_stats.game_durations_plot(df_player_games, string=True)
	df_yasuo = aggregate_stats.their_yasuo_vs_your_yasuo(df_ally_champion_winrates, df_enemy_champion_winrates)

	return {
		'account_name': account_name,
		'account_id': account_id,
		'oldest': oldest,
		'newest': newest,
		'player_champion_winrates': df_player_champion_winrates.to_dict(orient='index'),
		'ally_champion_winrates': df_ally_champion_winrates.to_dict(orient='index'),
		'enemy_champion_winrates': df_enemy_champion_winrates.to_dict(orient='index'),
		'blue_red_winrate': df_blue_red_winrate.to_dict(orient='index'),
		'joined_player_games': df_player_games.set_index('game_id').to_dict(orient='index'),
		'game_durations': {' '.join(k): v['average_duration'] for k, v in df_game_durations.to_dict(orient='index').items()},
		'game_durations_plot': image_game_durations_plot,
		'yasuo_table': df_yasuo.to_dict(orient='index'),
	}

def internal_generate_dataframes(account_id):
	'''generate dataframes using games/players stored in database'''
	db = get_db()
	df_player_games = pd.read_sql(
		f'''
		SELECT p.*, g.queue, g.duration, g.winner, g.forfeit, g.creation
		FROM players p INNER JOIN games g ON p.game_id = g.game_id
		WHERE p.player_id = "{account_id}"
		''',
		con=db
	)
	df_player_games.game_id.to_sql('matchlist', con=db, if_exists='append', index=False)
	df_other_players = pd.read_sql(
		f'''
		SELECT p.*
		FROM players p INNER JOIN matchlist m ON p.game_id = m.game_id
		WHERE p.player_id != "{account_id}"
		''',
		con=db
	)
	return df_player_games, df_other_players

def external_generate_dataframes(account_id, df_player_games, df_other_players):
	'''
	using dataframes from internal_generate_dataframes as a starting point,
	adds new games from riot api to both these dataframes and to the database
	'''
	db = get_db()
	df_new_games = riot_api.get_matchlist(account_id)
	df_new_games = df_new_games[~df_new_games.game_id.isin(df_player_games.game_id)]

	df_new_games.game_id.to_sql('new_matchlist', con=db, if_exists='append', index=False)
	df_games_to_collect = pd.read_sql(
		f'''
		SELECT nm.game_id
		FROM new_matchlist nm LEFT OUTER JOIN games g ON nm.game_id = g.game_id 
		WHERE g.game_id IS NULL
		''',
		con=db
	)
	df_new_games = df_new_games[df_new_games.game_id.isin(df_games_to_collect.game_id)]

	if df_new_games.empty:
		return df_player_games, df_other_players

	df_collected_matches = riot_api.get_matches(df_new_games)
	df_new_games['winner'] = np.where(
		df_collected_matches.teams.apply(lambda x: x[0]['win'] == 'Win'),
		100, 200
	)
	df_new_games['duration'] = df_collected_matches.gameDuration
	df_new_games['forfeit'] = riot_api.get_forfeits(df_new_games)
	
	# filter out remakes
	df_new_games, df_remakes = riot_api.filter_remakes(df_new_games)
	df_collected_matches, _ = riot_api.filter_remakes(df_collected_matches)

	player_ids, champion_ids, teams, game_ids = [], [], [], []
	df_collected_matches.participantIdentities.apply(
		lambda x: player_ids.extend(
			i['player']['accountId'] for i in x
		)
	)
	df_collected_matches.participants.apply(
		lambda x: champion_ids.extend(
			i['championId'] for i in x
		)
	)
	df_collected_matches.participants.apply(
		lambda x: teams.extend(
			i['teamId'] for i in x
		)
	)
	df_collected_matches.game_id.apply(
		lambda x: game_ids.extend(
			x for _ in range(10)
		)
	)
	df_new_players = pd.DataFrame(
		{'game_id': game_ids, 'player_id': player_ids, 'champion_id': champion_ids, 'team': teams} #'win': df_new_games.winner == wins}
	)
	df_new_players['win'] = df_new_players.apply(lambda x: int(x.team == df_new_games.loc[x.game_id, 'winner']), axis=1)
	df_new_players.drop(columns=['team'], inplace=True)

	df_new_games.to_sql('games', con=db, if_exists='append', index=False)
	df_remakes.to_sql('games', con=db, if_exists='append', index=False)
	df_new_players.to_sql('players', con=db, if_exists='append', index=False)

	df_new_other_players = df_new_players[df_new_players.player_id != account_id]
	df_new_desired_player = df_new_players[df_new_players.player_id == account_id]

	df_new_player_games = df_new_games.merge(
		df_new_desired_player, left_index=True, right_on='game_id'
	)
	df_new_player_games.drop(
		columns=['game_id_x', 'game_id_y'], inplace=True
	)

	df_player_games = df_player_games.append(df_new_player_games, ignore_index=True)
	df_other_players = df_other_players.append(df_new_other_players, ignore_index=True)

	return df_player_games, df_other_players
