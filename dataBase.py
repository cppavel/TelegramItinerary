import sqlite3

class DataBase:

    #creates a user database and sets a connection
    def __init__(self):
        self.connection = sqlite3.connect("users.db",check_same_thread=False)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("""CREATE TABLE users(userName text)""")
            self.connection.commit()
        except:
            print("Already created")

    #checking whether the user already exists
    def checkUsernameExists(self, userName):
        sql = "SELECT * FROM users WHERE userName=?"
        self.cursor.execute(sql, [(userName)])
        data = self.cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    #adding user
    def addUser(self, userName):
        if not self.checkUsernameExists(userName):
            sql = "INSERT INTO users VALUES (?)"
            self.cursor.execute(sql, [(userName)])
            self.connection.commit()
            return True
        else:
            return False

    #creating events table
    def createEventsTable(self):
        try:
            self.cursor.execute("""CREATE TABLE events(owner text, name text, category text,
            description text,date integer )""")
            self.connection.commit()
        except:
            print("Already created")

    #creating tasks table
    def createTasksTable(self):
        try:
            self.cursor.execute("""CREATE TABLE tasks(owner text, name text, category text,
            description text,deadline integer,status text )""")
            self.connection.commit()
        except:
            print("Already created")

    #adding event
    def addEvent(self, id, name,category,description,date):
        sql = "INSERT INTO events VALUES (?,?,?,?,?)"
        self.cursor.execute(sql, (id,name,category,description,date))
        self.connection.commit()

    #adding task
    def addTask(self,id,name,category,description,deadline,status):
        sql = "INSERT INTO tasks VALUES (?,?,?,?,?,?)"
        self.cursor.execute(sql, (id, name, category, description, deadline,status))
        self.connection.commit()

    #deleting event
    def deleteEvent(self, id, name, date):
        sql = "DELETE FROM events WHERE owner=? AND name=? AND date=?"
        self.cursor.execute(sql,(id,name,date))
        self.connection.commit()

    #deleting task
    def deleteTask(self, id, name, deadline):
        sql = "DELETE FROM tasks WHERE owner=? AND name=? AND deadline=?"
        self.cursor.execute(sql, (id, name, deadline))
        self.connection.commit()

    #deleting user
    def deleteUser(self,id):
        sql = "DELETE FROM events WHERE owner=?"
        self.cursor.execute(sql,[(id)])
        sql = "DELETE FROM tasks WHERE owner=?"
        self.cursor.execute(sql, [(id)])
        sql = "DELETE FROM users WHERE userName=?"
        self.cursor.execute(sql,[(id)])
        self.connection.commit()

    #getting events by dates and category
    def getEvents(self,id,date1,date2,category):
        if date1 + date2 != -2  and category != "none":
            sql = "SELECT * FROM events WHERE owner=? AND date>? AND date<? AND category=?"
            self.cursor.execute(sql,(id,date1,date2,category))
        elif date1 + date2 != -2:
            sql = "SELECT * FROM events WHERE owner=? AND date>? AND date<?"
            self.cursor.execute(sql, (id,date1,date2))
        elif category != "none":
            sql = "SELECT * FROM events WHERE owner=? AND category=?"
            self.cursor.execute(sql, (id,category))
        else:
            sql = "SELECT * FROM events WHERE owner=? "
            self.cursor.execute(sql, [(id)])
        data = self.cursor.fetchall()
        return data

    #getting tasks by deadline, category and completion status
    def getTasks(self,id,deadline,category,status):
        if deadline != -1 and category != "none":
            sql = "SELECT * FROM tasks WHERE owner=? AND deadline<? AND category=? AND status=?"
            self.cursor.execute(sql, (id,deadline, category,status))
        elif deadline != -1:
            sql = "SELECT * FROM tasks WHERE owner=? AND deadline<? AND status=?"
            self.cursor.execute(sql, (id,deadline,status))
        elif category !="none":
            sql = "SELECT * FROM tasks WHERE owner=? AND category=? AND status=?"
            self.cursor.execute(sql, (id,category,status))
        else:
            sql = "SELECT * FROM tasks WHERE owner=? AND status=?"
            self.cursor.execute(sql, (id, status))
        data = self.cursor.fetchall()
        return data

    #changing the status of an event
    def changetaskStatus(self,id,name,deadline,status):
        sql = "UPDATE tasks SET status=? WHERE owner =? AND name=? AND deadline=? "
        self.cursor.execute(sql, (status,id, name, deadline))
        self.connection.commit()