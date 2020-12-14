from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource


from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import current_app as app
import pandas as pd

from lol_online.db import get_db
from . import riot_api, aggregate_stats, table_manipulation

import sqlite3
import json
import sys

api = Api(app)

class HelloApi(Resource):
	def get(self):
		return {'data': 'hello!'}

class AllGames(Resource):
	def get(self):
		db = get_db()
		data = db.execute('SELECT * FROM games').fetchall()
		# return {'table': {row['game_id']: {k: v for k, v in dict(row).items() if k != 'game_id'} for row in data}}
		return {row['game_id']: {k: v for k, v in dict(row).items() if k != 'game_id'} for row in data}

class AllGamesLimited(Resource):
	def get(self, limit):
		db = get_db()
		data = db.execute('SELECT * FROM games LIMIT ?', [limit]).fetchall()
		# return {'table': {row['game_id']: {k: v for k, v in dict(row).items() if k != 'game_id'} for row in data}}
		return {row['game_id']: {k: v for k, v in dict(row).items() if k != 'game_id'} for row in data}

class AllPlayers(Resource):
	def get(self):
		db = get_db()
		data = db.execute('SELECT * FROM players').fetchall()		
		# return {'table': {i: dict(row) for i, row in enumerate(data)}}
		return {i: dict(row) for i, row in enumerate(data)}

class AllPlayersLimited(Resource):
	def get(self, limit):
		db = get_db()
		data = db.execute('SELECT * FROM players LIMIT ?', [limit]).fetchall()
		# return {'table': {i: dict(row) for i, row in enumerate(data)}}
		return {i: dict(row) for i, row in enumerate(data)}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlayerStats(Resource):
	def get(self, username):
		x = table_manipulation.generate_player_stats(username)
		print(sys.getsizeof(str(x)))
		return x

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

api.add_resource(HelloApi, '/hello_api')

api.add_resource(AllGames, '/all_games')
api.add_resource(AllGamesLimited, '/all_games/<limit>')
api.add_resource(AllPlayers, '/all_players')
api.add_resource(AllPlayersLimited, '/all_players/<limit>')

api.add_resource(PlayerStats, '/player_stats/<username>')

