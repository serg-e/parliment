from start_db import Session
from mapped_classes import *
from get_divisions import get_division_cd
session = Session()
divi = session.query(Division).first()



