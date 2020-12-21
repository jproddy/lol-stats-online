from flask import current_app as app
from flask_restful import Api, Resource

from lol_online.db import get_db
from . import table_manipulation

api = Api(app)


class HelloApi(Resource):
	def get(self):
		return {'data': 'hello!'}

class AllGames(Resource):
	def get(self):
		db = get_db()
		data = db.execute('SELECT * FROM games').fetchall()
		return {row['game_id']: {k: v for k, v in dict(row).items() if k != 'game_id'} for row in data}

class AllGamesLimited(Resource):
	def get(self, limit):
		db = get_db()
		data = db.execute('SELECT * FROM games LIMIT ?', [limit]).fetchall()
		return {row['game_id']: {k: v for k, v in dict(row).items() if k != 'game_id'} for row in data}

class AllPlayers(Resource):
	def get(self):
		db = get_db()
		data = db.execute('SELECT * FROM players').fetchall()		
		return {i: dict(row) for i, row in enumerate(data)}

class AllPlayersLimited(Resource):
	def get(self, limit):
		db = get_db()
		data = db.execute('SELECT * FROM players LIMIT ?', [limit]).fetchall()
		return {i: dict(row) for i, row in enumerate(data)}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PlayerStatsInternal(Resource):
	def get(self, username):
		return table_manipulation.generate_player_stats(username, True)

class PlayerStatsExternal(Resource):
	def get(self, username):
		return table_manipulation.generate_player_stats(username, False)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

api.add_resource(HelloApi, '/hello_api')

api.add_resource(AllGames, '/all_games')
api.add_resource(AllGamesLimited, '/all_games/<limit>')
api.add_resource(AllPlayers, '/all_players')
api.add_resource(AllPlayersLimited, '/all_players/<limit>')

api.add_resource(PlayerStatsInternal, '/player_stats_internal/<username>')
api.add_resource(PlayerStatsExternal, '/player_stats_external/<username>')
