# http://stackoverflow.com/questions/14906764/how-to-redirect-stdout-to-file-and-console-with-scripting


# http://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/  <-- how to run at startup

"""
You can use shell redirection while executing the python file:

python foo_bar.py > file
This will write all results being printed on stdout from the python source to file to the logfile.

Or if you want logging from within the script, you can try this:
"""

import sys

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger()


"""

Now you can use:

print("Hello")
This will write "Hello" to both stdout and the logfile

"""