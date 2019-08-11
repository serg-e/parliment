
from commons.kmodes import *
from commons.data_exploration import *
from commons.db import *
from commons.populate_db import *
import numpy as np

# session = Session()
# mps = session.query(MP).all()
# test_array = make_mp_votes_array(mps, eu_divisions)
# frame , modes = kmodes(test_array,4)
#
#


if __name__ == "__main__":
    mps = Session.query(MP).all()
    current_mps = Session.query(MP).filter(MP.person_id.in_(mps_current()))
    print(set(mps)-set(current_mps))
