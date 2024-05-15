import sqlite3
import sys
from typing import List, Optional
# import plugins
import plugins.capture as capture
import plugins.organize as organize
#import plugins.review as review

# connect to SQLite database
conn = sqlite3.connect('gtd.db')
c = conn.cursor()

# captures
# id | idea | created | archived
# 1  | Foo  | 1234    | 0
#
c.execute('''CREATE TABLE if not exists captures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea TEXT not null,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived INTEGER default 0)''')



# tasks
# id | name        | description | due_date | part_of | depends_on | created        | completed | completed_date
# 1  | Groceries   |              | 1234     | 2       | null       | 2018-01-01     | 0         | null
# 2  | Call Mom    |              | 1235     | 3       | 1          | 2018-01-02     | 1         | 2018-01-03
# 3  | Open Porch  |              |          | 4       | null       | 2018-01-04     | 0         | null
#
c.execute('''CREATE TABLE if not exists tasks ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT not null,
            description TEXT,
            due_date text,
            part_of INTEGER references captures (id),
            depends_on INTEGER references tasks(id),
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed INTEGER default 0,
            completed_date timestamp,
            archived INTEGER default 0)''')

conn.commit()
conn.close()

COMMANDS = {
    
    ## capture
    "-c": (capture.capture, 2), # idea
    "-cl": (capture.print_captures, 0),
    "-cla": (capture.print_captures_active, 0),
    "-ca": (capture.archive_capture, 2), # id
    "-cd": (capture.delete_capture, 2), # id

    ## organize
    "-t": (organize.new_task, 5), # name, description, due_date, part_of
    "-tnd": (organize.new_task_no_date, 4), # name, description, part_of
    "-tco": (organize.complete_task, 2), # id
    "-tdw": (organize.print_tasks_due_this_week, 0),
    "-tdm": (organize.print_tasks_due_this_month, 0),
    "-tl": (organize.print_tasks, 0),
    "-tla": (organize.print_tasks_active, 0),
    "-tlc": (organize.print_tasks_completed, 0),
    "-tld": (organize.print_dependent_tasks, 0),
}

def main():
    if len(sys.argv) < 2:
        print("Usage: gtd.py " + " | ".join(COMMANDS.keys()))
    else:
        command = sys.argv[1]
        if command in COMMANDS:
            function, num_args = COMMANDS[command]
            args = sys.argv[2:2+num_args]
            function(*args)
        else:
            print("Unknown command: " + command)


main()
