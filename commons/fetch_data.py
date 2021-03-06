import pandas as pd
from bs4 import BeautifulSoup as bs
import bs4
import requests
import numpy as np
from urllib.parse import urlencode, urlparse, parse_qs
import os



def generate_deivision_url(date, div_number, display='allpossible'):
	'''returns the url containing division table, both the date
		division number required. date format: YYYY-MM-DD'''

	base_url = 'https://www.publicwhip.org.uk/division.php?'
	params = {'date':date, 'number':div_number, 'display':display}
	return base_url + urlencode(params)


def download_division_table(url):
	'''requires full division url, downloads division data and returns dataframe
	'''
	page=requests.get(url)
	soup = bs(page.content, 'html.parser')
	table = soup.find('table', class_='votes', id='votetable')
	data = []
	for line in table.children:
	    if isinstance(line,bs4.element.Tag):
	        for column in line.children:
	            data.append(column.get_text())
	data = np.array(data)
	num_lines = int(len(data)/4)
	data=data.reshape(num_lines,4)
	frame =pd.DataFrame(data=data[1:,...], columns=data[0])
	return frame

def get_division(date, div_number, url=None):
	''' date: YYYY-MM-DD, division number required, dowloads data and outputs data frame
		source url: https://www.publicwhip.org.uk/division.php?
	'''
	# path = os.path.join('data', str(div_number))

	# try:
	# 	frame = pd.read_csv(path)
	# 	return frame
	#
	# except FileNotFoundError:
	if not url:
		url = generate_deivision_url(date,div_number)

	frame = download_division_table(url)
	frame['Party']=frame.Party.apply(parse_party)
	frame['division_number'] = div_number
	frame['date'] = pd.to_datetime(date)
	frame['url'] = url
	frame = frame.rename(columns={'Vote':'vote'})

	# frame.to_csv(path)
	return frame


def parse_party(string):
	''' standerdise party names from table'''
	parties = ['Con', 'Lab', 'SNP', 'Independent', 'LDem', 'DUP', 'SF', 'PC', 'Green', 'Speaker']
	for i in parties:
	    if i in string:
	        return i
	return np.nan

def download_divisions_index(url='https://www.publicwhip.org.uk/divisions.php'):
	''' download table of divisions: date, number, title, house'''
	page=requests.get(url)
	soup = bs(page.content, 'html.parser')
	table =soup.find('table', class_='votes')
	data = []
	for i in table.find_all('a',href=True):
	    div_dict = parse_qs(urlparse(i['href']).query)

	    try:
	        div_dict['house']
	        div_dict = {key:value[0] for key, value in div_dict.items()}
	        div_dict['title'] = i.get_text()
	        data.append(div_dict)
	    except KeyError:
	        continue
	frame = pd.DataFrame(data)
	frame['division_number']=frame.number.astype(int)
	frame.drop(axis=1,inplace=True, columns=['number'])
	return frame

# if __name__ =='__main__':
# 	divs = download_divisions_index()
# 	divs.division_numner
# 	divs.head()
