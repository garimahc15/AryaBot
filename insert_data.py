import psycopg2
from connectdb import config

def insert_feedback(username, first_name, last_name, user_feedback):
    """ insert a new feedback received from user via aryaacbot into the feedback table """
    sql_query = """ INSERT INTO feedback(username, first_name, last_name, user_feedback)
              VALUES(%s, %s, %s, %s) RETURNING user_id; """

    conn = None
    user_id = None
    try:
        # read database configuration
        params = config()
        
        #connect to the PostgreSQL database
        conn = psycopg2.connect(**params)

        #create a new cursor
        cur = conn.cursor()

        #execute the INSERT statement
        cur.execute(sql_query, (username, first_name, last_name, user_feedback))

        #get the generated serial id back
        #user_id = cur.fetchone()[0]

        #commit the changes to the database
        conn.commit()

        #close the communication with the database
        cur.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    #return user_id


def insert_question(username, first_name, last_name, user_question):
    """ insert a new feedback received from user via aryaacbot into the feedback table """
    sql_query = """ INSERT INTO question(username, first_name, last_name, user_question)
              VALUES(%s, %s, %s, %s) RETURNING user_id; """

    conn = None
    user_id = None
    try:
        # read database configuration
        params = config()

        #connect to the PostgreSQL database
        conn = psycopg2.connect(**params)

        #create a new cursor
        cur = conn.cursor()

        #execute the INSERT statement
        cur.execute(sql_query, (username, first_name, last_name, user_question))

        #get the generated serial id back
        #user_id = cur.fetchone()[0]

        #commit the changes to the database
        conn.commit()

        #close the communication with the database
        cur.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    #return user_id
