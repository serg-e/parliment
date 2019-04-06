from sqlalchemy import create_engine
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from twfy import twfy
from sqlalchemy.orm import sessionmaker
from get_divisions import get_division
from fuzzywuzzy import fuzz

from mapped_classes import *


division  = get_division('2019-03-27',393)


def add_mps(session):
	mps = twfy.getMPS()
	select_atrr = ['member_id','person_id','name','party', 'constituency']
	for mp in mps:
		mp_data = {key:mp[key] for key in select_atrr}
		session.add(MP(**mp_data))


def get_id_fuzz(name,session):
    '''lazy needs work, fuzzy compare input name with list of MP names in DB 
    	returns person_id'''
    for mp_name, person_id, in session.query(MP.name, MP.person_id).all():
        if fuzz.partial_token_sort_ratio(name,mp_name) ==100:
            return person_id
    raise Exception('person_id not found for {}'.format(name))

def add_division(div_frame, session):
	div_frame['person_id']=div_frame.Name.apply(lambda name : get_id_fuzz(name,session))
	assert len(div_frame[div_frame.person_id.isnull()==False])!=0, "not all MPs assigned id"

	select_atrr = ['person_id','vote', 'division_number']
	for i, vote in div_frame.iterrows():
		vote_data = {key:vote[key] for key in select_atrr}
		session.add(Vote(**vote_data))


if __name__ == '__main__':
	pass
	
 



