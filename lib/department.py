from __init__ import CURSOR, CONN  # Assuming these are global database connection objects

class Department:

    all = {}  # Dictionary to store Department instances for quick retrieval

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.id = None  # Initialize ID as None

    @classmethod
    def create_table(cls):
        """Creates the departments table if it doesn't exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drops the departments table if it exists."""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Saves the Department instance to the database and assigns it an ID."""
        sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid  # Retrieve the newly assigned ID
        Department.all[self.id] = self  # Add instance to the dictionary

    @classmethod
    def create(cls, name, location):
        """Creates a new department row in the database and returns a Department instance."""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Updates the department's corresponding database row with new attribute values."""
        if self.id is not None:  # Check if the instance has a valid ID
            sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.location, self.id))
            CONN.commit()

    def delete(self):
        """Deletes the department's corresponding database row."""
        if self.id is not None:  # Check if the instance has a valid ID
            sql = "DELETE FROM departments WHERE id = ?"
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            del Department.all[self.id]  # Remove from dictionary after deletion

    @classmethod
    def instance_from_db(cls, row):
        """Takes a table row and returns a Department instance."""
        if row is not None:  # Check if the row is not None
            return cls(row[1], row[2])  # Assuming name is at index 1 and location at index 2
        return None

    @classmethod
    def get_all(cls):
        """Returns a list of Department instances for every row in the db."""
        sql = "SELECT * FROM departments"
        results = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in results] if results else []

    @classmethod
    def find_by_id(cls, id):
        """Returns a Department instance corresponding to the db row retrieved by id."""
        sql = "SELECT * FROM departments WHERE id = ?"
        result = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(result) if result else None

    @classmethod
    def find_by_name(cls, name):
        """Returns a Department instance corresponding to the db row retrieved by name."""
        sql = "SELECT * FROM departments WHERE name = ?"
        result = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(result) if result else None
