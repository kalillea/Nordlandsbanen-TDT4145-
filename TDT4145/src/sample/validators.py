from operations import read


def user_in_database(id):
    users = [i[0] for i in read("""SELECT CustomerID FROM Customer""")]

    if id in users:
        return True
    return False
