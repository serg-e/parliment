from commons.twfy import twfy
from commons.fetch_data import get_division,download_divisions_index
from commons.mapped_classes import *
from sqlalchemy.exc import IntegrityError

from datetime import date



# division  = get_division('2019-03-27',393)


def add_mps(session,date=date.today()):
	mps = twfy.getMPS(date=date)
	print('new mps from twfy...')
	select_atrr = ['member_id','person_id','name','party', 'constituency']
	for mp in mps:
		try:
			mp_data = {key:mp[key] for key in select_atrr}
			session.add(MP(**mp_data))
			session.flush()
			session.commit()
			print(mp['name'], 'added')
		except IntegrityError:
			session.rollback()


def mps_current(date=date.today()):
	mps = twfy.getMPS(date=date)
	mp_ids = [int(mp['person_id']) for mp in mps ]
	return mp_ids



def find_id_from_name(name,session, date):
	matchs =[]
	name = str(name).strip()

	try:
		person_id = session.query(MP.person_id).filter(MP.name==name)[0][0]
		# print('person id found {}'.format(person_id))
		return person_id

	except IndexError:
		print('Missing MP:{}...loading mps as on {}'.format(name, date))
		add_mps(session, date=date)
		session.commit()
		person_id = session.query(MP.person_id).filter(MP.name==name)[0][0]
		print('person id found {}'.format(person_id))
		return person_id





def add_division(div_frame, session):

	#get person id from database by matching name
	date = div_frame['date'].iloc[0]
	div_frame['person_id']=div_frame.Name.apply(lambda name : find_id_from_name(name,session,date))

	if len(div_frame[div_frame.person_id.isnull()==True])!=0:
		print("not all MPs assigned id")
		print('missing {}'.format(div_frame[div_frame.person_id.isnull()==True]))

	select_atrr = ['person_id','vote', 'division_number']

	added = 0

	add_div = div_frame[select_atrr].copy()
	records = add_div[(add_div.person_id!='none')&(add_div.person_id.isnull()==False)].to_dict(orient='records')

	session.bulk_insert_mappings(Vote,records)
	session.commit()




def bulk_add_divisions(session,divs=None ,house='commons'):
	if not divs: divs = download_divisions_index()
	'''divs: dataframe with column for date and division number'''
	divs = divs[divs.house==house].copy()

	divs_in_db = [num[0] for num  in session.query(Vote.division_number).distinct()]
	divs = divs[~divs.division_number.isin(divs_in_db)].copy()

	if len(divs)==0:
		print('No divisions to add')
		return None

	div_frames = (get_division((row['date']), row['division_number']) for index, row in divs.iterrows())
	print('Adding {} divisions'.format(len(divs)))
	added =0
	for div in div_frames:
		add_division(div,session)
		added +=1
		print('{} divsions added of {}'.format(added,len(divs)), end='\r')

	populate_dvisions(session)
	update_div_titles(session)
	session.commit()
	start_date = min(divs.date)
	end_date = max(divs.date)
	print('All divisions from {} to {} added to database'\
	.format(start_date,end_date))



def update_div_titles(session,divs_info=None):
	divs_to_update = session.query(Division).filter(Division.title==None).all()
	if not divs_info:
		divs_info = download_divisions_index()
	for div in divs_to_update:
		try:
			div.title= divs_info[divs_info.division_number==div.division_number]['title'].iloc[0]
		except IndexError:
			print('No title found for division numner {}'.format(div.division_number))
			continue



def populate_dvisions(session):
	divs = [num[0] for num  in session.query(Vote.division_number).distinct()]
	for div in divs:
		try:
			session.add(Division(division_number=div))
			session.flush()
		except IntegrityError:
			session.rollback()

if __name__ == '__main__':


	print('Done')


''' check that each divsion contains all votes'''
