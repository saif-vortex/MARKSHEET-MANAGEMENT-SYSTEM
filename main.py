import database
import interface

if __name__ == "__main__":
    database.initialize_database()
    interface.start_app()