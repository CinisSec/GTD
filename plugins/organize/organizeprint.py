import sqlite3
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
            print(task[0], task[1], task[2], task[6], printable_completed)
        else:
            print(task[0], task[1], task[2], task[3], task[6], printable_completed)
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