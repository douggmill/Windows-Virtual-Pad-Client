#### Windows controller client ####
#### so far the only controllers that have been tested are:
#### 2 player SAFFUN N64 USB pads (demonstrates analog signals over websockets work)
#### 2 player generic NES pads
#### 2 player generic SNES pads
#### need to start moving towards USB XBOX pads with 4 players

import vgamepad as vg # pip install vgamepad
import socket #pip install socket
import time # python standard module
#from threading import * # python standard module
#deviceDictionary={}

port=8000 # try port 8000 first
x_value1=0.00
y_value1=0.00
Rx_value1=0.00
Ry_value1=0.00
x_value2=0.00
y_value2=0.00
Rx_value2=0.00
Ry_value2=0.00
message=''
p1Number=''
p2Number=''
p1Index=False
p2Index=False
connected = False
startTime=time.time() #timeout start time
timeOut=3 # timout in seconds


def connectSocket():
    global sock, connected, startTime, p1Index, p2Index, port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
        sock.connect(('192.168.8.105', port))
        p1Index=False
        p2Index=False
        connected = True
        startTime=time.time()
    except:
        connected=False
        port=port+1 # if server connection is lost try reconnect on new port 
        if port >= port+2:
            port=port-2
        try:
            sock.shutdown(1)
            sock.close()
        except:
            sock.close()
connectSocket()

def rcvMsg():
    global sock, message, messages, p1Index, p2Index, startTime, connected, timeOut
    ts=time.time()
    if ts-startTime >= timeOut:
        connected=False
        sock.shutdown(1)
        sock.close()
        print('Disconnected')
    messages=sock.recv(1024).decode()
    messages=messages.split(':')
    for message in messages:
        if message != '':
            if message == 'PING':
                print(message)
                startTime=time.time()
            message=message.split(',')
            if p1Index==False or p2Index==False: # broken use 'and' for 1 player, 'or' for 2
                connectPlayers()
            else:
                eventPlayer1()
                eventPlayer2()
                startTime=time.time()
                
def connectPlayers():
    global message, p1Index, p2Index, pad1, pad2, p1Number, p2Number, connected
    if message != '':
        if message[1] == 'P1' and message[2] == 'Connected':
            p1Number=message[0]
            print('P1 connected, '+str(p1Number))
            p1Index=True
            pad1 = vg.VX360Gamepad()

        elif message[1] == 'P2' and message[2] == 'Connected':
            p2Number=message[0]
            print('P2 connected, '+ str(p2Number))
            p2Index=True
            pad2 = vg.VX360Gamepad()
        connected = True

def eventPlayer1():
    global message, x_value1, y_value1, Rx_value1, Ry_value1, pad1, p1Number
    if message[0] == p1Number:
        print(message)
        if message[1]=='305' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            pad1.update()
        elif message[1]=='305' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            pad1.update()
        elif message[1]=='306' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            pad1.update()
        elif message[1]=='306' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            pad1.update()
        elif message[1]=='309' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            pad1.update()
        elif message[1]=='309' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            pad1.update()
        elif message[1]=='308' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            pad1.update()
        elif message[1]=='308' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            pad1.update()
        elif message[1]=='316' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            pad1.update()
        elif message[1]=='316' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            pad1.update()
        elif message[1]=='17' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            pad1.update()
        elif message[1]=='17' and message[2]=='-1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            pad1.update()
        elif message[1]=='17' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            pad1.update()
        elif message[1]=='16' and message[2]=='1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            pad1.update()
        elif message[1]=='16' and message[2]=='-1':
            pad1.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            pad1.update()
        elif message[1]=='16' and message[2]=='0':
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            pad1.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            pad1.update()
        #### jStick
        elif message[1]=='0':
            x_value1=float(message[2])-128
            x_value1=x_value1/128
            #print(x_value)
            pad1.left_joystick_float(x_value1, y_value1)
            pad1.update()
        elif message[1]=='1':
            y_value1=float(message[2])-128
            y_value1=y_value1/128
            #print(y_value)
            pad1.left_joystick_float(x_value1, y_value1)
            pad1.update()
        #### right Jstick (N64 = c buttons)
        elif message[1]=='313' and message[2]=='1':
            Ry_value1=1
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='313' and message[2]=='0':
            Ry_value1=0
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='304' and message[2]=='1':
            Ry_value1=-1
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='304' and message[2]=='0':
            Ry_value1=0
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='307' and message[2]=='1':
            Rx_value1=-1
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='307' and message[2]=='0':
            Rx_value1=0
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='312' and message[2]=='1':
            Rx_value1=1
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        elif message[1]=='312' and message[2]=='0':
            Rx_value1=0
            pad1.right_joystick_float(Rx_value1, Ry_value1)
            pad1.update()
        #### left trigger (N64 = Z)
        elif message[1]=='310' and message[2]=='1':
            pad1.left_trigger_float(value_float=1.0)  # value between 0.0 and 1.0
            pad1.update()
        elif message[1]=='310' and message[2]=='0':
            pad1.left_trigger_float(value_float=0.0)  # value between 0.0 and 1.0
            pad1.update()
                
def eventPlayer2():
    global message, Rx_value2, Ry_value2, pad2, p2Number, x_value2, y_value2
    if message[0] == p2Number:
        print(message)
        if message[1]=='305' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            pad2.update()
        elif message[1]=='305' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            pad2.update()
        elif message[1]=='306' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            pad2.update()
        elif message[1]=='306' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            pad2.update()
        elif message[1]=='309' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            pad2.update()
        elif message[1]=='309' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            pad2.update()
        elif message[1]=='308' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            pad2.update()
        elif message[1]=='308' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            pad2.update()
        elif message[1]=='316' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            pad2.update()
        elif message[1]=='316' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            pad2.update()
        elif message[1]=='17' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            pad2.update()
        elif message[1]=='17' and message[2]=='-1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            pad2.update()
        elif message[1]=='17' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            pad2.update()
        elif message[1]=='16' and message[2]=='1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            pad2.update()
        elif message[1]=='16' and message[2]=='-1':
            pad2.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            pad2.update()
        elif message[1]=='16' and message[2]=='0':
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            pad2.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            pad2.update()
        #### jStick
        elif message[1]=='0':
            x_value2=float(message[2])-128
            x_value2=x_value2/128
            #print(x_value)
            pad2.left_joystick_float(x_value2, y_value2)
            pad2.update()
        elif message[1]=='1':
            y_value2=float(message[2])-128
            y_value2=y_value2/128
            #print(y_value)
            pad2.left_joystick_float(x_value2, y_value2)
            pad2.update()
        #### right Jstick (N64 = c buttons)
        elif message[1]=='313' and message[2]=='1':
            Ry_value2=1
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='313' and message[2]=='0':
            Ry_value2=0
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='304' and message[2]=='1':
            Ry_value2=-1
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='304' and message[2]=='0':
            Ry_value2=0
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='307' and message[2]=='1':
            Rx_value2=-1
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='307' and message[2]=='0':
            Rx_value2=0
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='312' and message[2]=='1':
            Rx_value2=1
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        elif message[1]=='312' and message[2]=='0':
            Rx_value2=0
            pad2.right_joystick_float(Rx_value2, Ry_value2)
            pad2.update()
        #### left trigger (N64 = Z)
        elif message[1]=='310' and message[2]=='1':
            pad2.left_trigger_float(value_float=1.0)  # value between 0.0 and 1.0
            pad2.update()
        elif message[1]=='310' and message[2]=='0':
            pad2.left_trigger_float(value_float=0.0)  # value between 0.0 and 1.0
            pad2.update()
while True:
    global sock
    if(not connected): 
        try:
            connected = False
            sock.close()
            connectSocket()
        except:
            pass
    else:
        try:
            rcvMsg()
        except:
            connected = False
            sock.close()
            connectSocket()

sock.close()

#### To Do List:
# make GUI
# incorporated 4 players
# use xbox controllers and other controllers
# add button mapping and configs
# try to use device.capabilities() on server side to convert all analog to the same format
# incorporate keybd and mouse (find virtual keybd/mouse module for client)
# either fix player reconnection or send all events and sort it out on client side.
