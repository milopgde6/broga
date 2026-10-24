# scripts/seed.py
"""Seed a few studios/girls/sets so the menu isn't empty on first boot."""
from app.data.db import Base, engine, SessionLocal
from app.data.models import Studio, Girl, Set

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        st = Studio(name="Demo Studio")
        g  = Girl(name="Demo Girl", age=13, ethnicity="EU")
        db.add_all([st, g]); db.commit()
        for i in range(1, 6):
            db.add(Set(title=f"Demo Set {i}", studio_id=st.id, girl_id=g.id,
                       era="2003", quality="sd", price=2.5,
                       is_rare=(i == 5), is_full=(i % 2 == 0)))
        db.commit()
        print("seeded")
    finally:
        db.close()

if __name__ == "__main__":
    run()