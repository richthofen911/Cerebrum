#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'richthofen80'

import web
import shlex
import datetime
import subprocess
import time

urls = (
    '/cmd/(.*)', 'cmd'
)


class cmd:
    def GET(self, cmd_string):
        input_times = web.input(times=1)
        if not cmd_string:
            cmd_string = 'Command Not Found'
        for c in xrange(int(input_times.times)):
            return exec_cmd(cmd_string)


def exec_cmd(cmd_string, cwd=None, timeout=None, shell=False):
    if shell:
        cmd_string_list = cmd_string
    else:
        cmd_string_list = shlex.split(cmd_string)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # if output pipeline is not defined, it will be printed on the screen
    sp_new_cmd_process = subprocess.Popen(cmd_string_list, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=shell, bufsize=4096)

    # subprocess.poll() checks if sub process is finished. If so, set returncode and put it into subprocess.returncode
    while sp_new_cmd_process.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmd_string)
    cmd_result = sp_new_cmd_process.stdout.read()
    # return str(sp_new_cmd_process.returncode)
    return cmd_result


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
