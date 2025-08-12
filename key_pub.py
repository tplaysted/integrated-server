# Key publisher in python

import zmq
from pynput import keyboard
from enum import Enum
import argparse as ap

# Command enums
Lon = Enum('Lon', [('still', 0), ('forward', 1), ('back', 2)])
Lat = Enum('Lat', [('center', 0), ('left', 1), ('right', 2)])

wasd = {'w': False, 'a': False, 's': False, 'd': False} # keep track of wasd keys

def send_cmd(): # get the current state of wasd keys and sends a command
    # w/s for pure forward backward
    # a/d for pivot left/right
    # wa/wd for arc forward left/right
    # sa/sd for arc backward left/right
    # a-d and w-s cancel out if pressed at the same time
    lon = Lon.still
    lat = Lat.center

    # first determine the type of lateral/longitudinal movement the user wants

    if wasd['w'] and not wasd['s']:
        lon = Lon.forward

    if wasd['s'] and not wasd['w']:
        lon = Lon.back

    if wasd['a'] and not wasd['d']:
        lat = Lat.left

    if wasd['d'] and not wasd['a']:
        lat = Lat.right

    # send the command based on the lat/lon combination

    if lon == Lon.forward and lat == Lat.center:
        return socket.send_string('cmd:forward')
    
    if lon == Lon.forward and lat == Lat.left:
        return socket.send_string('cmd:forwardleft')
    
    if lon == Lon.forward and lat == Lat.right:
        return socket.send_string('cmd:forwardright')
    
    if lon == Lon.back and lat == Lat.center:
        return socket.send_string('cmd:backward')
    
    if lon == Lon.back and lat == Lat.left:
        return socket.send_string('cmd:backwardleft')
    
    if lon == Lon.back and lat == Lat.right:
        return socket.send_string('cmd:backwardright')
    
    if lon == Lon.still and lat == Lat.left:
        return socket.send_string('cmd:pivotleft')
    
    if lon == Lon.still and lat == Lat.right:
        return socket.send_string('cmd:pivotright')

    if lon == Lon.still and lat == Lat.center:
        return socket.send_string('cmd:still')


def on_press(key, injected): # executes whenever a key is pressed
    try:
        if key.char in 'wasd':
            wasd[key.char] = True
            send_cmd()
    except AttributeError:
        pass

def on_release(key, injected): # executes whenever a key is released
    try:
        if key.char in 'wasd':
            wasd[key.char] = False
            send_cmd()
    except AttributeError:
        pass

if __name__=="__main__":
    parser = ap.ArgumentParser(description='Listens to WASD key commands and publishes corresponding control actions.')
    parser.add_argument('-i', '--interface', 
                        type=str,
                        help='Start the publisher on a specific interface. Default is all (*)')
    parser.add_argument('-p', '--port', 
                        type=int,
                        help='Start the publisher on a specific port. Default is 5555')
    
    args = parser.parse_args()
    context = zmq.Context()

    interface = '*' if args.interface is None else args.interface
    port = '5555' if args.port is None else str(args.port)

    #  Socket to talk to server
    print('Binding server to socket...')
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://' + interface + ':' + port)
    print(f'Publishing to port {port} on interface {interface} ...')

    while True:
        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()


