import paho.mqtt.client as mqtt

topic_to_sub_status = 'device_status'
topic_to_sub_task_result = 'task_result'
topic_to_pub = 'center_command'
online_nodes_list = {}


# rc is the abbr. of result code
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = str(msg.payload)
    print(topic + ' | ' + payload)
    if topic == 'device_status':
        device_info = payload.split('::')
        device_name = device_info[0]
        device_status = device_info[1]
        if device_status == 'online':
            if online_nodes_list[device_name] is None:
                online_nodes_list[device_name] = device_status
            else:
                print('Duplicate device detected')
        else:
            if online_nodes_list[device_name] is None:
                print('Device not found')
            else:
                del online_nodes_list[device_name]
    else: # else means the topic is task result
        print('Task result: ' + msg.payload)


def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribe to topic')

        
client = mqtt.Client('Center')
client.on_connect = on_connect
client.on_message = on_message


client.connect("192.168.128.57", 1883, 60)
client.subscribe(topic_to_sub_status, qos=2)
client.subscribe(topic_to_sub_task_result, qos=2)

client.loop_forever()
