from sqlalchemy import create_engine
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from twfy import twfy
from sqlalchemy.orm import sessionmaker
from get_divisions import get_division,download_divisions_index
from fuzzywuzzy import fuzz
from start_db import Session
from mapped_classes import *
from sqlalchemy.exc import IntegrityError
from datetime import date



# division  = get_division('2019-03-27',393)


def add_mps(session,date=date.today()):
	mps = twfy.getMPS(date=date)
	select_atrr = ['member_id','person_id','name','party', 'constituency']
	for mp in mps:
		try:
			mp_data = {key:mp[key] for key in select_atrr}
			session.add(MP(**mp_data))
			session.flush()
		except IntegrityError:
			session.rollback()
	session.commit()


def get_id_fuzz(name,session):
	matchs =[]
	for mp_name, person_id, in session.query(MP.name, MP.person_id).all():
		if fuzz.partial_token_sort_ratio(name,mp_name) ==100:
			return person_id
		else:
			matchs.append(fuzz.partial_token_sort_ratio(name,mp_name))
	closest = max(matchs)
	closestd_id = matchs.index(max(matchs))
	cname = [mp.name for mp in  session.query(MP).all()][closestd_id]
	print('person_id not found for {0}, {1} closest{2}'.format(name,closest,cname))
	return 'none'

'''lazy needs work, fuzzy compare input name with list of MP names in DB
	returns person_id'''


def add_division(div_frame, session):

	#get person id from database by matching name
	div_frame['person_id']=div_frame.Name.apply(lambda name : get_id_fuzz(name,session))

	assert len(div_frame[div_frame.person_id.isnull()==False])!=0, \
	"not all MPs assigned id"

	select_atrr = ['person_id','vote', 'division_number']

	added = 0
	lost = []

	for i, vote in div_frame.iterrows():
		vote_data = {key:vote[key] for key in select_atrr}

		if vote_data['person_id'] == 'none':
			continue
		try:
			session.add(Vote(**vote_data))
			session.flush()
			added +=1

		except IntegrityError:
			session.rollback()
			print('vote from division {} exists'.format(vote_data['division_number']))
	session.commit()
	# print('Added {} votes'.format(added))

'''
person_id not found for  Barry McElduff, 60 closestJake Berry
386 divsions added of 396, %
person_id not found for  Heidi Alexander, 73 closestHeidi Allen
person_id not found for  Paul Flynn, 70 closestPaul Farrelly
person_id not found for  Barry McElduff, 60 closestJake Berry
'''''



def bulk_add_divisions(divs,session, house='commons'):
	'''divs: dataframe with column for date and division number'''
	divs = divs[divs.house==house].copy()
	divs_in_db = [num[0] for num  in session.query(Vote.division_number).distinct()]
	divs = divs[~divs.division_number.isin(divs_in_db)].copy()
	div_frames = [get_division((row['date']), row['division_number']) for index, row in divs.iterrows()]
	print('All division data downloaded, adding. {} divisions'.format(len(div_frames)))
	added =0
	for div in div_frames:
		add_division(div,session)
		added +=1
		print('{0} divsions added of {1}, %'.format(added,len(div_frames), int(added/len(div_frames)*100)))



def update_div_titles(session,divs_info=None):
	divs_to_update = session.query(Division).filter(Division.title==None).all()
	if not divs_info:
		divs_info = download_divisions_index()
	for div in divs_to_update:
		try:
			div.title= divs_info[divs_info.division_number==div.division_number]['title'].iloc[0]
		except IndexError:
			print('No title found for division numner {}'.format(div.division_number))
	session.commit()

def populate_dvisions(session):
	divs = [num[0] for num  in session.query(Vote.division_number).distinct()]
	for div in divs:
		try:
			session.add(Division(division_number=div))
			session.flush()
		except IntegrityError:
			session.rollback()

if __name__ == '__main__':
	# session = Session()
	session = Session()
	get_id_fuzz('Paul Flynn',session)
	add_mps(session,date='2017-08-01')
	add_mps(session,date='2018-08-01')
	add_mps(session,date='2019-08-01')
	print('mps added')
	divs = download_divisions_index()
	bulk_add_divisions(divs,session)
	# bulk_add_divisions(divs,session)
	populate_dvisions(session)
	update_div_titles(session)

	print('Done')

''' check that each divsion contains all votes'''
