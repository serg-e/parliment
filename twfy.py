import requests
import 	json


# API = {'api':{
#        'convertURL':[('output', 'url',), ()],
#        'getConstituency':[('output', 'postcode',), ()],
#        'getConstituencies':[('output',), ('date', 'search', 'latitude', 'longitude', 'distance')],
#        'getMP':[('output',), ('postcode', 'constituency', 'id', 'always_return')],
#        'getMPInfo':[('output', 'id',), ('fields')],
#        'getMPsInfo':[('output', 'id',), ('fields')],
#        'getMPs':[('output',), ('date', 'party', 'search')],
#        'getLord':[('output', 'id',), ()],
#        'getLords':[('output',), ('date', 'party', 'search')],
#        'getMLAs':[('output',), ('date', 'party', 'search')],
#        'getMSP':[('output',), ('postcode', 'constituency', 'id')],
#        'getMSPs':[('output',), ('date', 'party', 'search')],
#        'getGeometry':[('output',), ('name',)],
#        'getCommittee':[('output', 'name',), ('date',)],
#        'getDebates':[('output', 'type',), ('date', 'search', 'person', 'gid', 'order', 'page', 'num')],
#        'getWrans':[('output',), ('date', 'search', 'person', 'gid', 'order', 'page', 'num')],
#        'getWMS':[('output',), ('date', 'search', 'person', 'gid', 'order', 'page', 'num')],
#        'getHansard':[('output',), ('search', 'person', 'order', 'page', 'num')],
#        'getComments':[('output',), ('date', 'search', 'user_id', 'pid', 'page', 'num')]} 
#         }

API_KEY = 'DGBon5FGVqESCwBGagEdjKKV'


class TWFY:

	def __init__(self, API_KEY,output='js'):
		self.url='https://www.theyworkforyou.com/api/'
		self.params = {}
		self.params['key'] = API_KEY
		self.params['output'] = output


	def getMPS(self, **kwargs):
		'''returns list of dicts, dict for each MP'''
		params = self.params
		response = requests.get(self.url + 'getMPS', params=params)
		return json.loads(response.text)


twfy=TWFY(API_KEY)


# t= TWFY(API_KEY,'js')

