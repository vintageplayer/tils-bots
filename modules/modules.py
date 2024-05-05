import psycopg2
from psycopg2 import Error

# Function to establish a connection to the PostgreSQL database
def create_connection(db_name, user, password, host, port):
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connection to the database successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Function to insert a record into the database
def insert_record(connection, record):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO til.notes (start_message_id, telegram_user_id, telegram_username, telegram_first_name, telegram_last_name, doc_text, telegram_creation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, record)
        connection.commit()
        print("Record inserted successfully")
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")

# Function to read records from the database
def read_records(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM til.notes")
        records = cursor.fetchall()
        print("Retrieved records:")
        for record in records:
            print(record)
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to update doc_text for a given start_message_id
def update_doc_text(connection, telegram_user_id, new_doc_text):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE til.notes
            SET doc_text = doc_text || '\n' || %s
            WHERE telegram_user_id = %s AND is_draft = true
        """, (new_doc_text, telegram_user_id))
        connection.commit()
        print("Doc_text updated successfully")
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")

# Function to retrieve a draft message by telegram_user_id
def retrieve_draft_message(connection, telegram_user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM til.notes
            WHERE telegram_user_id = %s AND is_draft = true
        """, (telegram_user_id,))
        record = cursor.fetchone()
        return record
        # print("Retrieved record:")
        # print(record)
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to retrieve a draft message by telegram_user_id
def retrieve_user_messages(connection, telegram_username):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM til.notes
            WHERE telegram_username = %s AND is_draft = true
        """, (telegram_username,))
        record = cursor.fetchone()
        return record
        # print("Retrieved record:")
        # print(record)
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to update doc_text for a given start_message_id
def mark_note_as_completed(connection, telegram_user_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE til.notes
            SET is_draft = false
            WHERE telegram_user_id = %s AND is_draft = true
        """, (telegram_user_id, ))
        connection.commit()
        print("Doc_text updated successfully")
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")

# Example usage
if __name__ == "__main__":
    # Modify these variables according to your database configuration
    dbname = os.getenv('NEXT_DBNAME')
    user = os.getenv('NEXT_DB_USER')
    password = os.getenv('NEXT_DB_PASSWORD')
    host = os.getenv('NEXT_DB_HOST')
    port = os.getenv('NEXT_DB_PORT')

    # Sample record to insert
    record_to_insert = (12345, 1620133321, "johndoe", "John", "Doe", "Sample document text", 123456789)

    # Connect to the database
    connection = create_connection(dbname, user, password, host, port)

    if connection:
        # Insert a record
        insert_record(connection, record_to_insert)
        
        # Update doc_text for a given start_message_id
        update_doc_text(connection, 12345, "Updated document text")

        # Read records
        read_records(connection)

        # Close the connection
        connection.close()