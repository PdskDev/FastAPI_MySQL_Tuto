from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE= 'mysql+pymysql://nadetdev:DevTuto123@localhost:3306/fastapi_app_db'

engine = create_engine(URL_DATABASE)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

