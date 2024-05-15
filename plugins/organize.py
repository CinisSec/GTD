import sqlite3

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

def new_task(name, description, due_date, part_of):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks(name, description, due_date, part_of) VALUES(?, ?, ?, ?)', (name, description, due_date, part_of))
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

def print_tasks():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,name,description,due_date,completed,part_of, (SELECT idea FROM captures WHERE id = part_of) AS capture_idea FROM tasks')
    for task in c:
        if task[4] == 1:
            printable_completed = "COMPLETED"
        else:
            printable_completed = "NOT-COMPLETED"
        if task[3] is None or task[3] == "":
            print(task[0], task[1], task[2], "(part of capture: {} )".format(task[6]), printable_completed)
        else:
            print(task[0], task[1], task[2], task[3], "(part of capture: {} )".format(task[6]), printable_completed)
    conn.close()

def print_tasks_completed():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,name,description,due_date FROM tasks WHERE completed = 1')
    for task in c:
        print(task[0], task[1], task[2], task[3])
    conn.close()

def print_tasks_active():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,name,description,due_date,depends_on FROM tasks WHERE completed = 0')
    for task in c:
        printable_depends_on = ""
        if task[4] is not None and task[4] != "":
            printable_depends_on = " (depends on: " + str(task[4]) + ")"
        print(task[0], task[1], task[2], task[3], printable_depends_on)
    conn.close()

def print_dependent_tasks():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,name,description,due_date,depends_on FROM tasks WHERE completed = 0')
    for task in c:
        printable_depends_on = ""
        if task[4] is not None and task[4] != "":
            printable_depends_on = " (Task " + str(task[4]) + " needs to be completed first)"
        print(task[0], task[1], task[2], task[3], printable_depends_on)
    conn.close()

def complete_task(id):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1, completed_date = CURRENT_TIMESTAMP WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Task '{}' completed".format(id))

def print_tasks_due_this_week():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,name,description,due_date FROM tasks WHERE completed = 0 AND due_date > CURRENT_TIMESTAMP AND due_date < CURRENT_TIMESTAMP + 7 ORDER BY due_date')
    for task in c:
        print(task[0], task[1], task[2], task[3])
    conn.close()

def print_tasks_due_this_month():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,name,description,due_date FROM tasks WHERE completed = 0 AND due_date > CURRENT_TIMESTAMP AND due_date < CURRENT_TIMESTAMP + 30 ORDER BY due_date')
    for task in c:
        print(task[0], task[1], task[2], task[3])
    conn.close()
