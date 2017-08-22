"""Nail trigger OSC client

This program sends left and right nail triggers to the sim
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5006,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  #client.send_message("/trigger/left_nail", 1.0)
  #client.send_message("/trigger/left_nail i 1.0", 1.0)
  #client.send_message("/trigger/left_nail i 1", 1.0)
  #time.sleep(10)
  #client.send_message("/trigger/left_nail i 0", 0.0)

  client.send_message("/trigger/left_nail", 1.0)
  client.send_message("/trigger/right_nail", 1.0)
  time.sleep(20)
  client.send_message("/trigger/left_nail", 0.0)
  client.send_message("/trigger/right_nail", 0.0)