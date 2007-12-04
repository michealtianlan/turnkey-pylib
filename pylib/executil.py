"""This module contains high-level convenience functions for safe
command execution that properly escape arguments and raise an
exception on error"""
import os
import sys
import commands

class ExecError(Exception):
    def __init__(self, command, exitcode, output=None):
        Exception.__init__(self, command, exitcode, output)

        self.command = command
        self.exitcode = exitcode
        self.output = output

    def __str__(self):
        str = "non-zero exitcode (%d) for command: %s" % (self.exitcode,
                                                          self.command)
        if self.output:
            str += "\n" + self.output
        return str

def _fmt_command(command, args):
    return command + " ".join([commands.mkarg(arg) for arg in args])

def system(command, *args):
    """Executes <command> with <*args> -> None
    If command returns non-zero exitcode raises ExecError"""

    sys.stdout.flush()
    sys.stderr.flush()

    command = _fmt_command(command, args)
    error = os.system(command)
    if error:
        exitcode = os.WEXITSTATUS(error)
        raise ExecError(command, exitcode)

def getoutput(command, *args):
    """Executes <command> with <*args> -> output
    If command returns non-zero exitcode raises ExecError"""
    
    command = _fmt_command(command, args)
    error, output = commands.getstatusoutput(command)
    if error:
        exitcode = os.WEXITSTATUS(error)
        raise ExecError(command, exitcode, output)

    return output

