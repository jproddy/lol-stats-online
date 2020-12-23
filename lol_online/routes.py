from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import current_app as app
import pandas as pd

from lol_online.db import get_db
from . import riot_api, aggregate_stats, table_manipulation

# this is bad.
DATAFRAMES = {}


@app.route('/hello_route')
def hello_route():
	return 'hello'

@app.route('/api_key')
def show_api_key():
	return riot_api.API_KEY

@app.route('/games')
def show_games_database():
	''' lists all games currently in database '''
	db = get_db()
	df = pd.read_sql('SELECT * FROM games', con=db)
	return render_template(
		'table.html',
		table_type='all games in database',
		length=len(df),
		table=df.to_html(index=False)
	)

@app.route('/players')
def show_players_database():
	''' lists all players currently in database '''
	db = get_db()
	df = pd.read_sql('SELECT * FROM players', con=db)
	return render_template(
		'table.html',
		table_type='all players in database',
		length=len(df),
		table=df.to_html(index=False)
	)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/df_games')
def show_players_games():
	return render_template(
		'table.html',
		table_type='all games played by player',
		length=len(DATAFRAMES['df_games']),
		table=DATAFRAMES['df_games'].to_html()
	) 

@app.route('/df_players')
def show_players_players():
	return render_template(
		'table.html',
		table_type='all players in games played by player',
		length=len(DATAFRAMES['df_players']),
		table=DATAFRAMES['df_players'].to_html(index=False)
	)

@app.route('/joined_player_games')
def show_joined_players_games():
	return render_template(
		'table.html',
		table_type='joined player games',
		length=len(DATAFRAMES['df_joined_player_games']),
		table=DATAFRAMES['df_joined_player_games'].to_html()
	)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/player_champion_winrates')
def show_player_champion_winrates():
	return render_template(
		'table.html',
		table_type='player champion winrates',
		length=len(DATAFRAMES['df_player_champion_winrates']),
		table=DATAFRAMES['df_player_champion_winrates'].sort_values('p_value').to_html()
	)

@app.route('/ally_champion_winrates')
def show_ally_champion_winrates():
	return render_template(
		'table.html',
		table_type='ally champion winrates',
		length=len(DATAFRAMES['df_ally_champion_winrates']),
		table=DATAFRAMES['df_ally_champion_winrates'].sort_values('p_value').to_html()
	)

@app.route('/enemy_champion_winrates')
def show_enemy_champion_winrates():
	return render_template(
		'table.html',
		table_type='enemy champion winrates',
		length=len(DATAFRAMES['df_enemy_champion_winrates']),
		table=DATAFRAMES['df_enemy_champion_winrates'].sort_values('p_value').to_html()
	)

@app.route('/ally_enemy_champion_winrate_differential')
def show_ally_enemy_champion_winrate_differential():
	return render_template(
		'table.html',
		table_type='ally/enemy champion winrate differential',
		length=len(DATAFRAMES['df_yasuo']),
		table=DATAFRAMES['df_yasuo'].sort_values('delta_winrate').to_html()
	)

@app.route('/blue_red_winrate')
def show_blue_red_winrate():
	return render_template(
		'table.html',
		table_type='blue/red winrate',
		length=len(DATAFRAMES['df_blue_red_winrate']),
		table=DATAFRAMES['df_blue_red_winrate'].rename({100: 'blue', 200: 'red'}).to_html()
	)

@app.route('/game_duration_data')
def show_game_duration_data():
	return render_template(
		'table_and_plot.html',
		table_type='game duration data',
		length=len(DATAFRAMES['df_game_durations']),
		table=DATAFRAMES['df_game_durations'].to_html(),
		plot=DATAFRAMES['image_game_durations_plot']
	)

@app.route('/general_stats')
def show_general_stats():
	return render_template(
		'general_stats.html',
		oldest=DATAFRAMES['oldest'],
		newest=DATAFRAMES['newest']
	)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		account_name = request.form['account_name'].replace(' ', '')
		if account_name.isalnum() and 3 <= len(account_name) <= 16:
			try:
				session['account_name'] = account_name
				session['account_id'] = riot_api.get_account_id(account_name)
				session['internal_db_only'] = 'internal_db_only' in request.form
				return redirect(url_for('user_home'))
			except:
				flash('invalid account name', 'info')
				return render_template('home.html')
		else:
			flash('invalid account name', 'info')
			return render_template('home.html')
	else:
		if 'account_name' in session:
			return redirect(url_for('user_home'))
		return render_template('home.html')

@app.route('/user_home')
def user_home():
	if 'account_name' in session:
		if not session.get('populated', False):
			global DATAFRAMES
			DATAFRAMES = table_manipulation.generate_player_stats_route(session['account_name'], session['internal_db_only'])
		return render_template('user_home.html', length=len(DATAFRAMES['df_games']))

	else:
		return redirect(url_for('home'))

@app.route('/logout')
def logout():
	# session.pop('account_name', None)
	# session.pop('internal_db_only', None)
	session.clear()
	flash('switching account', 'info')
	return redirect(url_for('home'))
