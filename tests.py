from kmodes import *
from data_exploration import *
from start_db import *

session = Session()
mps = session.query(MP).all()
test_array = make_mp_votes_array(mps, eu_divisions)


k = 4

frame, modes = kmodes(test_array , 4)



err = []

if __name__ == '__main__':
    for i in range(100):
        kmodes(test_array , 4)
