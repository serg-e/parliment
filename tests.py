from kmodes import *
from data_exploration import *
from start_db import *
import numpy as np



if __name__ == "__main__":
    session = Session()
    mps = session.query(MP).all()
    test_array = make_mp_votes_array(mps, eu_divisions)
    for i in range(100):
        kmodes(test_array,4)
