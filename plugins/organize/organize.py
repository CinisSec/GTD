import sqlite3
import time

def new_task_no_date(name, description, part_of):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks(name, description, part_of) VALUES(?, ?, ?)', (name, description, part_of))
    c.execute('SELECT idea FROM captures  WHERE id = ?', (part_of,))
    for idea in c:
        dependency = idea[0]
    conn.commit()
    print("Task '{}' created (part of capture id: {})".format(name, dependency))
    conn.close()

def new_task(name, description, part_of, due_date):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    if due_date == "TODAY":
        due_date = time.strftime("%Y-%m-%d")
    c.execute('INSERT INTO tasks(name, description, part_of, due_date) VALUES(?, ?, ?, ?)', (name, description, part_of, due_date))
    conn.commit()
    print("Task '{}' created (part of capture id: {})".format(name, part_of))
    conn.close()

def delete_task(id):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Task '{}' deleted".format(id))


