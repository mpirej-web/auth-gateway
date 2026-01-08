import logging
import os
from auth_gateway import config
from auth_gateway import server
from auth_gateway import database

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting auth-gateway")

    db_url = os.getenv("DATABASE_URL", config.DEFAULT_DB_URL)
    db = database.connect(db_url)
    logging.info(f"Connected to database at {db_url}")

    auth_server = server.AuthServer(db)
    auth_server.start()

if __name__ == "__main__":
    main()