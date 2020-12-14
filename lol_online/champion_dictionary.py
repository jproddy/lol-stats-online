'''
provides dictionaries and functions to convert between a champions name and their internal id

import pandas as pd
df = pd.read_json('champion.json')
champ_to_id = dict(df.data.apply(pd.Series).key.astype(int))
id_to_champ = {v: k for k, v in champ_to_id.items()}
'''


champion_to_id_dict = {
	'Aatrox': 266,
	'Ahri': 103,
	'Akali': 84,
	'Alistar': 12,
	'Amumu': 32,
	'Anivia': 34,
	'Annie': 1,
	'Aphelios': 523,
	'Ashe': 22,
	'AurelionSol': 136,
	'Azir': 268,
	'Bard': 432,
	'Blitzcrank': 53,
	'Brand': 63,
	'Braum': 201,
	'Caitlyn': 51,
	'Camille': 164,
	'Cassiopeia': 69,
	'Chogath': 31,
	'Corki': 42,
	'Darius': 122,
	'Diana': 131,
	'DrMundo': 36,
	'Draven': 119,
	'Ekko': 245,
	'Elise': 60,
	'Evelynn': 28,
	'Ezreal': 81,
	'Fiddlesticks': 9,
	'Fiora': 114,
	'Fizz': 105,
	'Galio': 3,
	'Gangplank': 41,
	'Garen': 86,
	'Gnar': 150,
	'Gragas': 79,
	'Graves': 104,
	'Hecarim': 120,
	'Heimerdinger': 74,
	'Illaoi': 420,
	'Irelia': 39,
	'Ivern': 427,
	'Janna': 40,
	'JarvanIV': 59,
	'Jax': 24,
	'Jayce': 126,
	'Jhin': 202,
	'Jinx': 222,
	'Kaisa': 145,
	'Kalista': 429,
	'Karma': 43,
	'Karthus': 30,
	'Kassadin': 38,
	'Katarina': 55,
	'Kayle': 10,
	'Kayn': 141,
	'Kennen': 85,
	'Khazix': 121,
	'Kindred': 203,
	'Kled': 240,
	'KogMaw': 96,
	'Leblanc': 7,
	'LeeSin': 64,
	'Leona': 89,
	'Lillia': 876,
	'Lissandra': 127,
	'Lucian': 236,
	'Lulu': 117,
	'Lux': 99,
	'Malphite': 54,
	'Malzahar': 90,
	'Maokai': 57,
	'MasterYi': 11,
	'MissFortune': 21,
	'MonkeyKing': 62,
	'Mordekaiser': 82,
	'Morgana': 25,
	'Nami': 267,
	'Nasus': 75,
	'Nautilus': 111,
	'Neeko': 518,
	'Nidalee': 76,
	'Nocturne': 56,
	'Nunu': 20,
	'Olaf': 2,
	'Orianna': 61,
	'Ornn': 516,
	'Pantheon': 80,
	'Poppy': 78,
	'Pyke': 555,
	'Qiyana': 246,
	'Quinn': 133,
	'Rakan': 497,
	'Rammus': 33,
	'RekSai': 421,
	'Rell': 526,
	'Renekton': 58,
	'Rengar': 107,
	'Riven': 92,
	'Rumble': 68,
	'Ryze': 13,
	'Samira': 360,
	'Sejuani': 113,
	'Senna': 235,
	'Seraphine': 147,
	'Sett': 875,
	'Shaco': 35,
	'Shen': 98,
	'Shyvana': 102,
	'Singed': 27,
	'Sion': 14,
	'Sivir': 15,
	'Skarner': 72,
	'Sona': 37,
	'Soraka': 16,
	'Swain': 50,
	'Sylas': 517,
	'Syndra': 134,
	'TahmKench': 223,
	'Taliyah': 163,
	'Talon': 91,
	'Taric': 44,
	'Teemo': 17,
	'Thresh': 412,
	'Tristana': 18,
	'Trundle': 48,
	'Tryndamere': 23,
	'TwistedFate': 4,
	'Twitch': 29,
	'Udyr': 77,
	'Urgot': 6,
	'Varus': 110,
	'Vayne': 67,
	'Veigar': 45,
	'Velkoz': 161,
	'Vi': 254,
	'Viktor': 112,
	'Vladimir': 8,
	'Volibear': 106,
	'Warwick': 19,
	'Xayah': 498,
	'Xerath': 101,
	'XinZhao': 5,
	'Yasuo': 157,
	'Yone': 777,
	'Yorick': 83,
	'Yuumi': 350,
	'Zac': 154,
	'Zed': 238,
	'Ziggs': 115,
	'Zilean': 26,
	'Zoe': 142,
	'Zyra': 143,
}

id_to_champion_dict = {
    266: 'Aatrox',
    103: 'Ahri',
    84: 'Akali',
    12: 'Alistar',
    32: 'Amumu',
    34: 'Anivia',
    1: 'Annie',
    523: 'Aphelios',
    22: 'Ashe',
    136: 'AurelionSol',
    268: 'Azir',
    432: 'Bard',
    53: 'Blitzcrank',
    63: 'Brand',
    201: 'Braum',
    51: 'Caitlyn',
    164: 'Camille',
    69: 'Cassiopeia',
    31: 'Chogath',
    42: 'Corki',
    122: 'Darius',
    131: 'Diana',
    36: 'DrMundo',
    119: 'Draven',
    245: 'Ekko',
    60: 'Elise',
    28: 'Evelynn',
    81: 'Ezreal',
    9: 'Fiddlesticks',
    114: 'Fiora',
    105: 'Fizz',
    3: 'Galio',
    41: 'Gangplank',
    86: 'Garen',
    150: 'Gnar',
    79: 'Gragas',
    104: 'Graves',
    120: 'Hecarim',
    74: 'Heimerdinger',
    420: 'Illaoi',
    39: 'Irelia',
    427: 'Ivern',
    40: 'Janna',
    59: 'JarvanIV',
    24: 'Jax',
    126: 'Jayce',
    202: 'Jhin',
    222: 'Jinx',
    145: 'Kaisa',
    429: 'Kalista',
    43: 'Karma',
    30: 'Karthus',
    38: 'Kassadin',
    55: 'Katarina',
    10: 'Kayle',
    141: 'Kayn',
    85: 'Kennen',
    121: 'Khazix',
    203: 'Kindred',
    240: 'Kled',
    96: 'KogMaw',
    7: 'Leblanc',
    64: 'LeeSin',
    89: 'Leona',
    876: 'Lillia',
    127: 'Lissandra',
    236: 'Lucian',
    117: 'Lulu',
    99: 'Lux',
    54: 'Malphite',
    90: 'Malzahar',
    57: 'Maokai',
    11: 'MasterYi',
    21: 'MissFortune',
    62: 'MonkeyKing',
    82: 'Mordekaiser',
    25: 'Morgana',
    267: 'Nami',
    75: 'Nasus',
    111: 'Nautilus',
    518: 'Neeko',
    76: 'Nidalee',
    56: 'Nocturne',
    20: 'Nunu',
    2: 'Olaf',
    61: 'Orianna',
    516: 'Ornn',
    80: 'Pantheon',
    78: 'Poppy',
    555: 'Pyke',
    246: 'Qiyana',
    133: 'Quinn',
    497: 'Rakan',
    33: 'Rammus',
    421: 'RekSai',
    526: 'Rell',
    58: 'Renekton',
    107: 'Rengar',
    92: 'Riven',
    68: 'Rumble',
    13: 'Ryze',
    360: 'Samira',
    113: 'Sejuani',
    235: 'Senna',
    147: 'Seraphine',
    875: 'Sett',
    35: 'Shaco',
    98: 'Shen',
    102: 'Shyvana',
    27: 'Singed',
    14: 'Sion',
    15: 'Sivir',
    72: 'Skarner',
    37: 'Sona',
    16: 'Soraka',
    50: 'Swain',
    517: 'Sylas',
    134: 'Syndra',
    223: 'TahmKench',
    163: 'Taliyah',
    91: 'Talon',
    44: 'Taric',
    17: 'Teemo',
    412: 'Thresh',
    18: 'Tristana',
    48: 'Trundle',
    23: 'Tryndamere',
    4: 'TwistedFate',
    29: 'Twitch',
    77: 'Udyr',
    6: 'Urgot',
    110: 'Varus',
    67: 'Vayne',
    45: 'Veigar',
    161: 'Velkoz',
    254: 'Vi',
    112: 'Viktor',
    8: 'Vladimir',
    106: 'Volibear',
    19: 'Warwick',
    498: 'Xayah',
    101: 'Xerath',
    5: 'XinZhao',
    157: 'Yasuo',
    777: 'Yone',
    83: 'Yorick',
    350: 'Yuumi',
    154: 'Zac',
    238: 'Zed',
    115: 'Ziggs',
    26: 'Zilean',
    142: 'Zoe',
    143: 'Zyra',
}

def champion_to_id(champion):
	return champion_to_id_dict.get(champion, f'UNKNOWN_{champion}')

def id_to_champion(champion_id):
	return id_to_champion_dict.get(champion_id, f'UNKNOWN_{champion_id}')
