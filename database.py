from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(os.getenv("DATABASE_URL"))


SessionLocal = sessionmaker(bind=engine)

    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_conection(self):
    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão realizada com sucesso!")
            print(result.scalar())

    except Exception as e:
        print("❌ Erro ao conectar:")
        print(e)