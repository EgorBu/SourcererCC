#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function, unicode_literals
import subprocess
import sys
import os

# exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
# states
STATE_EXECUTE_1 = 0
STATE_INIT = 1
STATE_INDEX = 2
STATE_MOVE_INDEX = 3
STATE_EXECUTE_2 = 4
STATE_SEARCH = 5


class ScriptControllerException(Exception):
    pass


def run_command(cmd):
    print("running command {}".format(" ".join(cmd)))
    p = subprocess.Popen(cmd, universal_newlines=True)
    p.communicate()
    return p.returncode


def full_file_path(string):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), string)


def full_script_path(string, param=""):
    res = full_file_path(string)
    if param != "":
        res += " " + param
    return res


def run_command_wrapper(cmd, params):
    command = full_script_path(cmd, params)
    return_code = run_command(command.split())
    if return_code != EXIT_SUCCESS:
        raise ScriptControllerException("error during executing {}".format(command))


# Aim of this class is to run the scripts for SourcererCC with a single command
class ScriptController(object):
    def __init__(self, num_nodes):
        self.num_nodes_search = num_nodes
        self.script_meta_file_name = full_file_path("scriptinator_metadata.scc")
        self.current_state = STATE_EXECUTE_1  # default state
        self.previous_run_state = self.load_previous_state()

    def execute(self):
        print("previous run state {}".format(self.previous_run_state))
        if self.previous_run_state <= STATE_EXECUTE_1:
            run_command_wrapper("execute.sh", "1")
        self.current_state += 1
        self.flush_state()
        # execute the init command
        if self.previous_run_state <= STATE_INIT:
            if self.previous_run_state == STATE_INIT:
                # last time the execution failed at init step. We need to replace the existing gtpm index from the backup
                run_command_wrapper("restore-gtpm.sh", "")
            else:
                # take backup of existing gtpmindex before starting init
                run_command_wrapper("backup-gtpm.sh", "")
            # run the init step
            run_command_wrapper("runnodes.sh", "init 1")
        self.current_state += 1

        # execute index
        self.perform_step(STATE_INDEX, "runnodes.sh", "index 1")
        # execute move indexes
        self.perform_step(STATE_MOVE_INDEX, "move-index.sh", "")
        # execute command to create the dir structure
        self.perform_step(STATE_EXECUTE_2, "execute.sh", "{}".format(self.num_nodes_search))
        self.perform_step(STATE_SEARCH, "runnodes.sh", "search {}".format(self.num_nodes_search))

        self.flush_state()
        self.current_state = STATE_EXECUTE_1  # go back to EXE 1 state
        print("SUCCESS: Search Completed on all nodes")

    def perform_step(self, state, cmd, params):
        self.flush_state()
        if self.previous_run_state <= state:
            run_command_wrapper(cmd, params)
        self.current_state += 1

    def flush_state(self):
        print("flushing current state {}".format(self.current_state))
        with open(self.script_meta_file_name, "w", encoding="utf-8") as f:
            f.write("{}\n".format(self.current_state))

    def load_previous_state(self):
        print("loading previous run state")
        if os.path.isfile(self.script_meta_file_name):
            with open(self.script_meta_file_name, "r", encoding="utf-8") as f:
                return int(f.readline())
        else:
            print("{} doesn't exist, creating one with state EXECUTE_1".format(self.script_meta_file_name))
            return STATE_EXECUTE_1


if __name__ == '__main__':
    numnodes = 2
    if len(sys.argv) >= 2:
        numnodes = int(sys.argv[1])
    print("search will be carried out with {} nodes".format(numnodes))

    controller = ScriptController(numnodes)
    controller.execute()
