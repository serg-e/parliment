from commons import *
import os

# os.remove('commons.db')

session = Session()
add_mps(session)
bulk_add_divisions(session)
Session.remove()
