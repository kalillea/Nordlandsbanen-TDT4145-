from menu import main_menu
import shared


def main():
    print("""
          ------------------------------- \n
          Velkommen til Norske Baner Inc. \n
          En database for Norske baner. \n
          ------------------------------- \n
          """)
    shared.db_name = 'data/database.db'
    main_menu()


if __name__ == "__main__":
    main()
