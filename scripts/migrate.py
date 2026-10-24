#!/usr/bin/env python3
"""Create all tables. Idempotent."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.db import engine, Base
import app.data.models  # noqa: F401  (register models)


def main():
    Base.metadata.create_all(engine)
    print("✅ schema up to date")


if __name__ == "__main__":
    main()