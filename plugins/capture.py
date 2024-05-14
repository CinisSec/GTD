import sqlite3

def capture(idea):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('INSERT INTO captures (idea) VALUES(?)', (idea,))
    conn.commit()
    conn.close()
    print("Capture '{}' created".format(idea))

def print_captures():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,idea FROM captures')
    for capture in c:
        print(capture)
    conn.close()

def delete_capture(id):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    if id == "all":
        c.execute('DELETE FROM captures')
    else:
        c.execute('DELETE FROM captures WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Capture '{}' removed".format(id))
