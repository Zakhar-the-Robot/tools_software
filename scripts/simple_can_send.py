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
from brain_pycore.zmq import (ZmqPublisherThread, ZmqSubscriberThread, ZmqServerThread, ZmqClientThread)


def msg_to_dict(msg_str: str):
    id_data = msg_str.split("#")
    
    if len(id_data) != 2:
        print("Wrong msg format")
        return None
    
    id = int(id_data[0], 16)
    data = id_data[1]
    data_list = []
    while data:
        try:
            d = int(data[:2],16)
        except Exception as e:
            print(e)
            return None
        data_list.append(d)
        data = data[2:]
    return {"id":id, "data": data_list}
    

if __name__ == '__main__':
    CANBUS_SEND_SERVER_PORT = 5566
    # 
    cli = ZmqClientThread(port=CANBUS_SEND_SERVER_PORT,address="zakhar")
    cli.start()
    
    while 1:
        print("Message format, hex: ID#D0D1.... E.g. 701#01C2")
        inpt = input('Enter the message (empty for exit):')
        if not inpt:
            break
        msg = msg_to_dict(inpt)
        if msg is None: 
            continue
        resp = cli.send(str(msg))
        print(f"[{resp}]")

    cli.stop()
