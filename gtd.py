import sqlite3
import sys
from typing import List, Optional
# import plugins
import plugins.capture as capture
#import plugins.organize as organize
#import plugins.review as review

# connect to SQLite database
conn = sqlite3.connect('gtd.db')
c = conn.cursor()

# create tables
c.execute('''CREATE TABLE if not exists captures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea TEXT not null)''')

conn.commit()
conn.close()


def main():
    if len(sys.argv) == 0:
        print("Usage: gtd.py -c <idea> | -cl | -cd <id>")
    elif sys.argv[1] == "-c":
        capture.capture(sys.argv[2])
    elif sys.argv[1] == "-cl":
        capture.print_captures()
    elif sys.argv[1] == "-cd":
        capture.delete_capture(sys.argv[2])

main()
