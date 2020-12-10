
# This is a module designed to hit most aspects of a database

#  http://www.mysqltutorial.org/python-mysql/  is the source of this code
# this program uses data in the config.ini file to get db: name, user, host, password
#-------------------------------- IMPORT ------------------------------------
import mysql.connector
from mysql.connector import Error
from mysql.connector import cursor

from mysql.connector import MySQLConnection

from python_mysql_connect2 import connect
from python_mysql_connect2 import close
# python_mysql_connect2 only has the two methods connect and close
# it imports from python_mysql_dbconfig import read_db_config and
# from mysql.connector import MySQLConnection, Error


from python_mysql_dbconfig import read_db_config
# uses config parser and returns db info

#----------------------- VARIABLES --------------------------------------
mytable = "books"

#----------------- CONNECT ------------------------ 
# connect can be used if you want to avoid the ini file stuff, needs work
def connect_local(dbhost,dbname,dbuser,dbpword):
    """ Connect to MySQL database """
    x = input("Pause")
    conn = ()
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database= "mydb",
                                       user='pi',
                                       password='dorques')
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 


 


#------------------ FETCH ONE ----------------------------
def query_with_fetchone():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + mytable)
 
        row = cursor.fetchone()
 
        while row is not None:
            print(row)
            row = cursor.fetchone()
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()
 
 

#------------------ FETCH ALL ------------------------------
def query_with_fetchall():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + mytable )
        rows = cursor.fetchall()
 
        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()
 


#----------------- FETCH MANY -------------------------
# used to keep from loading the entire db into memory
def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row
def query_with_fetchmany():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
 
        cursor.execute("SELECT * FROM " + mytable)
 
        for row in iter_row(cursor, 10):
            print(row)
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()

#------------------ INSERT INTO TABLE --------------------------
def insert_table(title, isbn):

    query = "INSERT INTO " + mytable +"(title,isbn) " \
            "VALUES(%s,%s)"
    args = (title, isbn)
 
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        print("OK so far")
 
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()
# sample 

   #insert_book('A Sudden Light','9781439187036')

#------------------------------ INSERT MANY --------------------------
def insert_multi_table(mytable,in_col1,data1,in_col2,data2):
    #query = "INSERT INTO " + mytable +"(title,isbn) " \
    #        "VALUES(%s,%s)"
    query = "INSERT INTO {}({},{}) VALUES({},{})".format(mytable,in_col1,data1,in_col2,data2)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.executemany(query)
 
        conn.commit()
    except Error as e:
        print('Error:', e)
 
    finally:
        cursor.close()
        conn.close()
 

#    books = [('Harry Potter And The Order Of The Phoenix', '9780439358071'),
#             ('Gone with the Wind', '9780446675536'),
#             ('Pride and Prejudice (Modern Library Classics)', '9780679783268')]
#    insert_books(books)

#------------------------------ UPDATE ---------------------------------------
def update_table(mytable,set_col,set_value,where_col,where_value):
    # Passed variables useage: UPDATE {mytable} SET {set_col} = {set_value} WHERE {where_col} = {where_value}"
    # read database configuration
    db_config = read_db_config()
 


    # if the WHERE clause is a string it should be coded \"data\" to surround by quotes
    tquery = "UPDATE {} SET {} = {} WHERE {} = {}".format(mytable,set_col,set_value,where_col,where_value)
    
    print(tquery)
    try:
        conn = MySQLConnection(**db_config)
 
        # update set_col with set_val
        cursor = conn.cursor()

        cursor.execute(tquery)
        # accept the changes
        conn.commit()
 
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()
 
#    update_book(37, 'The Giant on the Hill *** TEST ***')
#It is important to understand that we should always use 
#placeholders ( %s) inside any SQL statements that contain input from users. This helps us prevent SQL injection.

#------------------------------ DELETE DATA -----------------------------------
def delete_record(mytable,delete_row,where_col,where_value):
    db_config = read_db_config()
 
    #query = "DELETE FROM books WHERE id = %s"
    query = "DELETE FROM {} WHERE {} = {}".format(mytable,delete_row,where_col,where_value)
 
    try:
        # connect to the database server
        conn = MySQLConnection(**db_config)
 
        # execute the query
        cursor = conn.cursor()
        cursor.execute(query, (book_id,))
 
        # accept the change
        conn.commit()
 
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()


#------------------------------- FIRE A DB STORED PROCEDURE ----------------------------------
def call_find_all_sp():
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
 
        cursor.callproc('find_all')
 
        # print out the result
        for result in cursor.stored_results():
            print(result.fetchall())
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()

#    call_find_all_sp()

#------------------------ RAW SQL INSERT, EDIT OR DELETE ----------------------------------------
# in this one you have to format the entire sql string and feed it in
def raw_sql_write(sql_statement):
    db_config = read_db_config()
 

    query = sql_statement
 
    try:
        # connect to the database server
        conn = MySQLConnection(**db_config)
 
        # execute the query
        cursor = conn.cursor()
        cursor.execute(query)
 
        # accept the change
        conn.commit()
 
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()



#---------------------- RAW SQL FETCH ---------------------------------------------
def raw_sql_read(sql_statement):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        rows = cursor.fetchall()
        sql_fetch = ()
 
        #print('Total Row(s):', cursor.rowcount)
        #print("Current sql = ",sql_statement)
        for row in rows:
            #print(row)
            sql_fetch = (sql_fetch + row)
            
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()
        #print("sql_fetch = ",sql_fetch)
        
        return sql_fetch
        
        

 

#---------------------------- ADD QUOTES ---------------------------------------------
# adds double quotes to string and returns it
def add_quotes(qstring):
    qstring = "\"" + qstring + "\""
    return qstring

#--------------------------------------------------------------------------------------


#////////////////////// START MAIN //////////////////////////////////
def main():
        if __name__ == '__main__':
            
            dbhost = "localhost"
            dbname = "mydb"
            dbuser = "pi"
            dbpword = "dorques"

            connect()
            select = input("Select 1 to write data, 2 Edit, 3 Update, 4 Read   ")
            if select == "1":
                print("1 selected")
                title = input("Title  ")
                num = input("Number  ")
                insert_table(title,num)
            if select == "2":
                pass
            if select == "3":
                data1 = input("Title is ")
                data1 = add_quotes(data1)
                data2 = input("isbn # is ")
                col1 = "title"
                col2 = "isbn"
                 
                sql_statement = "INSERT INTO {}({},{}) VALUES({},{})".format(mytable,col1,col2,data1,data2)  
                #update_table(mytable,"title","\"Corn Huskers\"","isbn",4)
                print(sql_statement)
                raw_sql_write(sql_statement)
            if select == "4":
                data1 = "title"
                sql_statement = "SELECT {} FROM {} ORDER BY {}".format(data1,mytable,data1)
                print("Titles  ",raw_sql_read(sql_statement))


            print(query_with_fetchall())
            


if __name__ == "__main__":
    # If this is being run stand-alone then execute otherwise it is being
    # imported and the importing program will use the modules it needs
   try:
        
        
        while True:
            2== 2 # guess this is usually true
   
            main() # Invoke the program    
                
            
            

   except KeyboardInterrupt:
        #cleanup at end of program
        close()
        print('   Shutdown')
        
else:
    print("sql_access loaded as module")
 




