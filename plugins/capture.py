import sqlite3

def capture(idea):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('INSERT INTO captures (idea) VALUES(?)', (idea,))
    conn.commit()
    conn.close()
    print("'{}' Captured".format(idea))

def print_captures():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,idea,created,archived FROM captures')
    for capture in c:
        if capture[3] == 0:
            printable_archive_status = "Active"
        else:
            printable_archive_status = "Archived"
        print(capture[0], capture[1], capture[2], printable_archive_status)
    conn.close()

def print_captures_active():
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('SELECT id,idea,created FROM captures WHERE archived = 0')
    for capture in c:
        print(capture[0], capture[1], capture[2])
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
    print("Capture '{}' deleted".format(id))

def archive_capture(id):
    conn = sqlite3.connect('gtd.db')
    c = conn.cursor()
    c.execute('UPDATE captures SET archived = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print("Capture '{}' archived".format(id))