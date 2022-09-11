#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************
from time import sleep
from brain_pycore.zmq import (ZmqClientThread)
from pynput import keyboard

CANBUS_SEND_SERVER_PORT = 5566

active = False
cli = ZmqClientThread(port=CANBUS_SEND_SERVER_PORT,address="zakhar")


def input_simple():
    inpt = input('Enter command (empty for exit):')
    
    if not inpt:
        print("Exit")
        return -1
    
    if len(inpt) > 1:
        print("Only one char")
        return 0
    
    return inpt

def send(client, cmd_char):
    msg = {"id":0x12F, "data": [ord(cmd_char)]}
    if msg is None: 
        return 0
    resp = client.send(str(msg))
    return resp
    
    
def on_press(key):
    # sleep(.1)
    try:
        send(cli, key.char)
    #     print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

if __name__ == '__main__':
    active = True
    
    cli.start()
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    
    while active:
        pass
        # print("Message format, hex: ID#D0D1.... E.g. 701#01C2")
        
        # inpt = input_simple()
        # if not inpt:
        #     continue
        # if inpt == -1:
        #     break
        
        # resp = send(cli, inpt)
        # print(f"[{resp}]")

    listener.stop()
    cli.stop()
