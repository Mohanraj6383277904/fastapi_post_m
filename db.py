from sqlalchemy import create_engine,MetaData

engine = create_engine("mysql://root@localhost:3306/new_ausweg_project")

meta = MetaData()

conn = engine.connect()

def get_db():
    try:
        yield conn
    except:
        conn.close()
        