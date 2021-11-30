from ctypes import sizeof
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import os
import os.path as osp
import sys
BUILD_DIR1 = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC/build/service/")
BUILD_DIR2 = osp.join(osp.dirname(osp.abspath(__file__)), "../../MQTT/build/service/")
sys.path.insert(0, BUILD_DIR1)
sys.path.insert(0, BUILD_DIR2)
import argparse

import grpc
import fib_pb2
import fib_pb2_grpc
import logs_pb2
import logs_pb2_grpc
import psutil
import paho.mqtt.client as mqtt
ip = '0.0.0.0'
grpc_port_fib = 8080
grpc_port_logs = 8081
mqtt_port = 1883
# Create your views here.
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'hello world' }, status=200)

class FiboView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        order = request.data["order"]
        # print(order)
        host = f"{ip}:{grpc_port_fib}"
        print(host)
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            fibo_request = fib_pb2.FibRequest()
            fibo_request.order = order

            fibo_response = stub.Compute(fibo_request)
            # print(response.value)
        client = mqtt.Client()
        client.connect(host=ip, port=mqtt_port)
        client.loop_start()
        client.publish(topic='logs', payload=order)

        return Response(data={"val": str(fibo_response.value)}, status=200)

class LogView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        host = f"{ip}:{grpc_port_logs}"
        with grpc.insecure_channel(host) as channel:
            stub = logs_pb2_grpc.LogsRetrieverStub(channel)
            logs_request = logs_pb2.LogsRequest()
            logs_response = stub.Compute(logs_request)
            # print(sys.getsizeof(logs_response))
            # print(sys.getsizeof(logs_response.value))
        return Response(data={"history": str(logs_response.value)}, status=200)
    
