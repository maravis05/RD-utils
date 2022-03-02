

import zmq
import time
blinks = []
onset = False

ctx = zmq.Context()
# The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
pupil_remote = ctx.socket(zmq.REQ)
print(pupil_remote)

ip = 'localhost'  # If you talk to a different machine use its IP.
port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.

pupil_remote.connect(f'tcp://{ip}:{port}')

# Request 'SUB_PORT' for reading data
pupil_remote.send_string('SUB_PORT')
sub_port = pupil_remote.recv_string()

# Request 'PUB_PORT' for writing data
pupil_remote.send_string('PUB_PORT')
pub_port = pupil_remote.recv_string()

subscriber = ctx.socket(zmq.SUB)
subscriber.connect(f'tcp://{ip}:{sub_port}')
subscriber.subscribe('pupil')  # receive all gaze messages

# we need a serializer
import msgpack

while True:
    topic, payload = subscriber.recv_multipart()
    now = time.localtime()
    message = msgpack.loads(payload)
    #print(f"{topic}: {message}")

    #when pupil confidence falls below .3 for the "first time", we grab onset time
    if (float(message['confidence']) < .3 and float(message['confidence']) > 0 and onset == False):
        onset = True
        blink_onset_time = now
    
    #when pupil is re-acquired after being lost, we grab pupil return time
    elif (float(message['confidence']) > .3 and onset == True):
        onset = False
        pupil_return_time = now

        #if the amount of time that the pupil was lost is greater than 1 second, we discard and start over.
        #if the pupil was lost for 1 second or less, we record the time of onset and the confidence, and print to screen.
        if (pupil_return_time.tm_sec()-blink_onset_time.tm_sec() <= 1):
            time_string = str(blink_onset_time.tm_hour) + ':' + str(blink_onset_time.tm_min) + ':' + str(blink_onset_time.tm_sec)
            confidence = message['confidence']
            blinks.append(confidence+" "+time_string)
            print(confidence+" "+time_string)









