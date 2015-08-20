#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'richthofen80'

import json
import urllib2
import os


def cmd_switch(cmd_master):
    cmd_args = cmd_master.split(' ')
    if cmd_args[0] == 'add':
        add(cmd_args[1])
    elif cmd_args[0] == 'add_machine':
        add_machine(cmd_args[1], cmd_args[2])
    elif cmd_args[0] == 'add_all':
        add_all()
    elif cmd_args[0] == 'remove':
        remove(cmd_args[1])
    elif cmd_args[0] == 'remove_all':
        remove_all()
    elif cmd_args[0] == 'ls_loaded':
        ls_loaded()
    elif cmd_args[0] == 'ls_all':
        ls_all()
    elif cmd_args[0] == 'exec':
        shoot_cmd(cmd_master[5:])
    else:
        print 'command not found'


def add(machine_name):
    global target_loaded
    global target_all
    target_loaded[machine_name] = target_all[machine_name]


def add_machine(machine_name, ip_addr):
    global target_all
    path_sys_home = os.environ['HOME']
    targets_file = path_sys_home + '/cerebrum_targets'
    try:
        with open(targets_file, 'w') as targets_file_operation:
            target_all[machine_name] = ip_addr
            json.dump([target_all], targets_file_operation)
        target_all[machine_name] = ip_addr
    except IOError:
        print 'targets_file open error'


def add_all():
    global target_loaded
    global target_all
    target_loaded = target_loaded.clear()
    target_loaded = target_all


def remove(machine_name):
    global target_loaded
    del target_loaded[machine_name]


def remove_all():
    global target_loaded
    target_loaded.clear()


def ls_loaded():
    global target_loaded
    for machine_name in target_loaded:
        print machine_name + ':\t', target_loaded[machine_name]


def ls_all():
    global target_all
    for machine_name in target_all:
        print machine_name + ':\t', target_all[machine_name]


def shoot_cmd(cmd_target):
    response_list = []
    global target_loaded
    for machine_name in target_loaded:
        # request_list.append(urllib2.Request(target_loaded[machine_name]))
        url_prefix = "http://"
        response = urllib2.urlopen(urllib2.Request(url_prefix + target_loaded[machine_name] + '/cmd/' + cmd_target))
        response_list.append(response.read())
        for resp in response_list:
            print resp + '\n'


def init_target_list():
    path_sys_home = os.environ['HOME']
    targets_file = path_sys_home + '/cerebrum_targets'
    try:
        targets_file_operation = open(targets_file, 'a+')
        content = targets_file_operation.read()
        if not content:
            json.dump([{'default': 'empty'}], targets_file_operation)
    except IOError:
        print 'targets_file open error'
    finally:
        targets_file_operation.close()


def load_local_json():
    path_sys_home = os.environ['HOME']
    targets_file = path_sys_home + '/cerebrum_targets'
    global target_all
    try:
        targets_file_operation = open(targets_file, 'a+')
        target_tmp = json.load(targets_file_operation)
        target_tmp = list(target_tmp)
        target_all = target_tmp[0]
        if 'default' in target_all.keys():
            del target_all["default"]
    except IOError:
        print 'targets_file open error'
    finally:
        targets_file_operation.close()


if __name__ == "__main__":
    global target_all
    target_all = {}
    global target_loaded
    target_loaded = {}
    init_target_list()
    load_local_json()
    cmd_this = raw_input('Cerebrum: ')
    while cmd_this != 'q':
        cmd_switch(cmd_this)
        cmd_this = raw_input('Cerebrum: ')



