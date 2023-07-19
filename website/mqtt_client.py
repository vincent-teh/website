from website.extensions import  mqtt_client, temp


'''
    MQTT publish is a blocking operation.
    Looping through a publish event will the system failed to send system
    level acknowledgement.
    It is advisable to never put loop pulish here.
'''
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        mqtt_client.subscribe('TEMP')
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect():
    print('Device disconnect')

@mqtt_client.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    if data['topic'] == 'TEMP':
        temp.put_temp(float(data['payload']))
        mqtt_client.publish('POWER', temp.get_power())
