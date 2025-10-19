import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemyseeder import ResolvingSeeder

from app.settings import DATABASE_URL

parser = argparse.ArgumentParser()

parser.add_argument('revision')
args = parser.parse_args()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with Session() as session:
    seeder = ResolvingSeeder(session)
    new_entities = seeder.load_entities_from_json_file(
        os.path.join(os.path.dirname(__file__), 'versions', f'{args.revision}.json')
    )
    session.commit()