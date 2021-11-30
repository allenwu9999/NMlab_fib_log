import time
import argparse

import psutil
import paho.mqtt.client as mqtt
import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import logs_pb2
import logs_pb2_grpc
import threading

ip = "0.0.0.0"
mqtt_port = 1883
grpc_port = 8081
history = []

class LogsServicer(logs_pb2_grpc.LogsRetrieverServicer):
    def __init__(self):
        pass
    def Compute(self, request, context):
        response = logs_pb2.LogsResponse()
        print(history)
        for i in history:
            response.value.append(i)
        # print(response.value)
        # print(str(response.value))
        return response

def on_message(client, obj, msg):
    history.append(int(msg.payload))
    # print(history)
    print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")                        

def subscriber():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host=ip, port=mqtt_port)
    client.subscribe('logs', 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogsServicer()
    logs_pb2_grpc.add_LogsRetrieverServicer_to_server(servicer, server)
    # subscriber()
    thr = threading.Thread(target=subscriber)
    thr.start()
    
    try:
        server.add_insecure_port(f"{ip}:{grpc_port}")
        server.start()
        print(f"Run gRPC Server at {ip}:{grpc_port}")
        server.wait_for_termination()
    except KeyboardInterrupt as e:
        pass