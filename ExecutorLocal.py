#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'richthofen80'

import shlex
import datetime
import subprocess
import time

'''
this function execute a shell command
args:
    cmd_string: the raw command in string form
    cwd:       if not None, it changes to the wanted path before cmdString is executed
    timeout:   precision can be 0.1
    shell:     if cmdString is executed through shell
'''


def exec_command(cmd_string, cwd=None, timeout=None, shell=False):
    if shell:
        cmd_string_list = cmd_string
    else:
        cmd_string_list = shlex.split(cmd_string)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # if output pipeline is not defined, it will be printed on the screen
    sp_new_cmd_process = subprocess.Popen(cmd_string_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096)

    # subprocess.poll() checks if sub process is finished. If so, set returncode and put it into subprocess.returncode
    while sp_new_cmd_process.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmd_string)

    return str(sp_new_cmd_process.returncode)

if __name__ == "__main__":
    print exec_command("ps -ef")

