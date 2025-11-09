import sqlite3
import os

# Set Current Working Directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#create Database if it does not exist
def create_database(db_name):

    print(f'Creating {db_name} Database.')
    with open(db_name, 'w') as fp: #opens and creates the file
        print('Database has been created.')

#create tasks table without any data
def create_table(db_name, table_name):
    try:
        #Ccnnect to the database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        #SQL query to create a table with all required fields
        query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    due_date TEXT,
                    priority INTEGER,
                    category TEXT,
                    created_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
                    updated_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )'''

        #execute the SQL query
        cursor.execute(query)
        print(f'The {table_name} table has been created')

    except sqlite3.Error as error:
        print(f'Error ocured - {error}') #print any SQLite-related errors

    #Always close the connection
    finally:
        if conn:
            conn.close()
            print('Table has been created')
            print('SQLite Connection closed')

#create or refresh final_project database
def main():
    dbname = 'final_project.db' #database file name
    table  = 'tasks' #table name

    exist_chk = os.path.exists(os.path.join(os.getcwd(), dbname)) #check if the database file already exists


    if exist_chk:
        print('Warning this will wipe out any existing data.')
        imp = input('Do you want to overwrite final_project Database? (y/n)')
        if imp.lower() == 'y':
            create_table(dbname, table) #if user says yes, re-create the table
        else:
            print('Exited program without Database being touched')

    #if DB doesn't exist, create both the file and the table
    else:
        create_database(dbname)
        create_table(dbname, table)



# Run the main function
if __name__ == "__main__":
    main()