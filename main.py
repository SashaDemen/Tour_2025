




from views import *


from db import engine, Base


Base.metadata.create_all(engine)