
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import column_property

Base = declarative_base()

class MP(Base):

	__tablename__ = 'MPs'
	name = Column(String)
	party = Column(String)
	person_id = Column(Integer, primary_key=True)
	member_id = Column(Integer)
	constituency = Column(String)

	divisions = association_proxy( 'votes','division')

	votes = relationship('Vote', back_populates='mp')
	# divisions = relationship('Division', secondary='votes',back_populates='mps' )


	def __repr__(self):
		return "<MP(name='%s', party='%s')>" % (self.name, self.party)



class Vote(Base):

	__tablename__ = 'votes'
	person_id = Column(Integer,ForeignKey('MPs.person_id') ,primary_key=True)
	division_number = Column(Integer, ForeignKey('divisions.division_number'), primary_key=True)
	vote = Column(String)
	
	division = relationship('Division')

	mp = relationship('MP', back_populates='votes')


	# division = relationship('Division', back_populates='votes')

	def __repr__(self):
		return "<Vote(name='%s', vote='%s')>" % (self.mp.name, self.vote)

class Division(Base):

	__tablename__ = 'divisions'

	division_number = Column(Integer, primary_key=True)
	votes = relationship('Vote', back_populates='division')
	mps = association_proxy('votes','mp')


	# url = Column(String)
	# votes = relationship('Division', back_populates='division')
	# mps = association_proxy('votes', 'mp' )

	@hybrid_property
	def ayes(self):
		return  list(filter(lambda vote: vote.vote=='aye', self.votes))

	@hybrid_property
	def noes(self):
		return  list(filter(lambda vote: vote.vote=='no', self.votes))

	@hybrid_property
	def abstentions(self):
		return  list(filter(lambda vote: vote.vote=='absent', self.votes))

	@hybrid_property
	def result(self):
		if len(self.ayes) > len(self.noes):
			return 'passed'
		else:
			return 'rejected'
	@hybrid_property
	def parties(self):
		parties = list(set([mp.party for mp in self.mps]))
		return parties

	@hybrid_property
	def party_ayes(self):
		'''returns dict of form 'party': number of aye votes'''
		return {party:len(list(filter(lambda vote : vote.mp.party==party,self.ayes))) for party in self.parties}

	@hybrid_property
	def party_noes(self):
		'''returns dict of form 'party': number of aye votes'''
		return {party:len(list(filter(lambda vote : vote.mp.party==party,self.noes))) for party in self.parties}











