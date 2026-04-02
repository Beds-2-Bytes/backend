from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

db_type = os.getenv('DBTYPE')


print("DBTYPE: ", db_type)

if db_type == 'postgres':

    DATABASE_URL = f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@{os.getenv('DBURL')}/{os.getenv('DBNAME')}"

elif db_type == 'mariadb':

    DATABASE_URL = f"mysql+pymysql://{os.getenv('DBUSER')}:{os.getenv('DBPW')}@{os.getenv('DBURL')}/{os.getenv('DBNAME')}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
