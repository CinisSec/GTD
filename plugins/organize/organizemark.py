import sqlite3
def mark_task_complete(id):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1, completed_date = CURRENT_TIMESTAMP WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Task '{}' completed".format(id))

def mark_task_incomplete(id):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 0, completed_date = null WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Task '{}' incomplete".format(id))