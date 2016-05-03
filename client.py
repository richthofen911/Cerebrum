import paho.mqtt.client as mqtt
import socket
import shlex
import datetime
import subprocess
import time

device_name = socket.gethostname().split('.')[0]
topic_to_sub = 'center_command'
topic_to_pub = 'online'


# rc is the abbr. of result code
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.publish(topic_to_pub, payload=device_name + '::online', qos=2, retain=False)


def on_disconnect(client, userdata, rc):
    print('disconnect')


def on_publish(client, userdata, mid):
    print str(userdata)



def on_message(client, userdata, msg):
    payload = str(msg.payload).split('|')
    target = payload[0]
    cmd = payload[1]
    if target == 'all' or target == device_name:
        if cmd == 'disconnect':
            client.publish(topic_to_pub, payload=device_name + '::offline', qos=2, retain=False)
            client.disconnect()
        else:
            exec_cmd(cmd)

        

def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribe to topic')


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


client = mqtt.Client(device_name)
client.on_connect = on_connect
client.on_message = on_message


client.connect("192.168.128.57", 1883, 60)
client.subscribe(topic_to_sub, qos=2)

client.loop_forever()
