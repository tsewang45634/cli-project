import sqlite3

def create_connection():
    try: 
        con = sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print(e)




def create_table(con):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name char(255) not null,
            last_name char(255) not null,
            company_name char(255) not null,
            address char(255) not null,
            city char(255) not null,
            county char(255) not null,
            state  char(255) not null,
            zip real  not null,
            phone1 char(255) not null,
            phone2 char(255),
            email char(255) not null,
            web text
        );
    """

    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY )
    print("Successfully created the table.")



INPUT_STRING = """
Enter the option:
    1. CREATE TABLE
    2. DUMP USERS FROM CSV INTO USERS TABLE
    3. ADD NEW USER INTO USERS TABLE
    4. QUERY ALL USERS FROM TABLE
    5. QUERY USER BY ID FROM TABLE
    6. QUERY SPECIFIED NO.OF RECORDS FROM TABLE
    7. DELETE ALL USERS
    8. DELETE USER BY ID
    9. UPDATE USER
    10. PRESS ANY KEY TO EXIT
 """

import csv 

def read_csv():
    users = []
    with open ('sample_users.csv') as f:
        data = csv.reader(f)
        for i in data:
            users.append(tuple(i))
    return users[1:]




def insert_users(con,users):
    user_add_query = """
    INSERT INTO USERS
    (
    first_name,
    last_name,
    company_name,
    address,
    city,
    county,
    state,
    zip,
    phone1,
    phone2,
    email,
    web

    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur = con.cursor()
    cur.executemany(user_add_query, users )
    con.commit()
    print(f"{len(users)} users were imported successfully.")


def select_users(con):
    cur = con.cursor()
    users = cur.execute('SELECT * FROM users')
    for user in users:
        print(user)


def select_users_by_id(con ,user_id):
    cur = con.cursor()
    users = cur.execute('SELECT * FROM users where id = ?;', (user_id,))
    for user in users:
        print(user)



def delete_users(con):
    cur = con.cursor()
    cur.execute("delete from users;")
    con.commit()
    print('all users were deleted successfully')




def delete_user_by_id(con,user_id):
    cur = con.cursor()
    cur.execute("delete from users where id = ?", (user_id,))
    con.commit()
    print(f"user with id [{user_id}] was successfully deleted.")



def select_users(con, limit=None):
    cur = con.cursor()
    if limit:
        users = cur.execute('select * from users limit ?', (limit,))
    else:
        users = cur.execute('select * from users')
    for user in users:
        print(user)

def update_user_by_id(con, user_id, column_name, column_value):
    update_query = f"update users set {column_name}=? where id = ?;"
    cur = con.cursor()
    cur.execute(update_query,(column_value, user_id))
    con.commit()
    print(
        f"[{column_name}] was updated with value [{column_value}] of user with id [{user_id}]"
    )

COLUMNS = (
        'first_name',
        'last_name',
        'company_name',
        'address',
        'city',
        'county',
        'state',
        'zip',
        'phone1',
        'phone2',
        'email',
        'web',
  
    
)

def main():
    con = create_connection()
    user_input = input(INPUT_STRING)
    if user_input == '1':
        create_table(con)

    elif user_input=="2":
        users = read_csv()
        insert_users (con, users)

    elif user_input== '3':
        user_data = []
        for column in COLUMNS:
            column_value = input(f'enter the value of {column}:')
            user_data.append(column_value)
        insert_users(con, [tuple(user_data)])
        

    elif user_input == '4':
        select_users(con)

    elif user_input == '5':
        user_id = input('enter the id of user:')
        if user_id.isnumeric():
            select_users_by_id(con, user_id)

    elif user_input == '6':
        limit = input("how many user you want to see?")
        if limit.isnumeric():
            select_users(con, limit)

    elif user_input == '7':
        confirmation = input('are you sure you want to delete all users? (y/n)')
        delete_users(con)

    elif user_input == '8':
        user_id = input('enter the id of user:')
        if user_id.isnumeric():
             delete_user_by_id(con,user_id)


    elif user_input == '9':
        user_id = input('enter id of user:')
        if user_id.isnumeric():
            column_name = input(
                f"ehter the column you want to edit. please make sure column is with in {COLUMNS}:"
            )
            if column_name in COLUMNS:
                column_value = input(f"ehter the value of {column_name}:")
                update_user_by_id(con, user_id, column_name, column_value)
    
    else:
        exit()


if __name__ == '__main__':
    main()