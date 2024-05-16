import sqlite3
import sys
# import plugins
import plugins.capture as capture
import plugins.organize.organize as organize
import plugins.organize.organizeprint as oprint
import plugins.organize.organizemark as omark

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

def overview():
    print("CAPTURES")
    capture.print_captures_active()
    print("\nTASKS")
    oprint.print_tasks()

COMMANDS = {
    ## overview
    "-o": (overview, 0),
    ## capture
    "-c": (capture.capture, 2), # idea
    "-cl": (capture.print_captures, 0),
    "-cla": (capture.print_captures_active, 0),
    "-ca": (capture.archive_capture, 2), # id
    "-cd": (capture.delete_capture, 2), # id
    ## organize
    ### task creation
    "-tcd": (organize.new_task, 5), # name, description, due_date, part_of
    "-tc": (organize.new_task_no_date, 4), # name, description, part_of
    ### task marking
    "-tmc": (omark.mark_task_complete, 2), # id
    "-tmi": (omark.mark_task_incomplete, 2), # id
    #"-tmar": (omark.mark_tasks_archive, 2), # id
    #### Task range marking
    #"-tmcr": (omark.mark_task_complete_range, 2), # start_id, end_id
    #"-tmir": (omark.mark_task_incomplete_range, 2), # start_id, end_id
    #"-tmar": (omark.mark_tasks_archive_range, 2), # start_id, end_id
    ### task deletion
    "-td": (organize.delete_task, 2), # id
    #"-tdr": (organize.delete_task_range, 2), # start_id, end_id
    ### task printing
    "-tdw": (oprint.print_tasks_due_this_week, 0),
    "-tdm": (oprint.print_tasks_due_this_month, 0),
    "-tl": (oprint.print_tasks, 0),
    "-tla": (oprint.print_tasks_active, 0),
    "-tlc": (oprint.print_tasks_completed, 0),
    "-tld": (oprint.print_dependent_tasks, 0),
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
