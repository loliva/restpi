#!/usr/bin/env python

import ConfigParser
import RPi.GPIO as GPIO
from flask import Flask, jsonify, url_for, abort, make_response, request
GPIO.setwarnings(False)

# Configuracion Base
config = ConfigParser.RawConfigParser()
config.read('gpio.cfg')

# Defino puertos
allowed_ports = ['port1', 'port2', 'port3', 'port4', 'port5', 'port6']

# Seteo GPIO
GPIO.setmode(GPIO.BOARD)

for port in allowed_ports:
    GPIO.setup(config.getint(port, 'gpio_pin'), GPIO.OUT)

# Crear objeto flask
app = Flask(__name__)

# Status del puerto
@app.route('/port/<input_port>', methods = ['GET'])
def port_get(input_port):
    port = input_port.lower()
    if (not _check_port(port)):
        abort(404)
    
    if(GPIO.input(config.getint(port, 'gpio_pin'))):
        return "On"
    else:
        return "Off"

# Puerto arriba
@app.route('/port/<input_port>/on', methods = ['PUT'])
def port_on(input_port):
    port = input_port.lower()
    if (not _check_port(port)):
        abort(404)
    
    
    GPIO.output(config.getint(port, 'gpio_pin'), True)
    return "On"

# Puerto Abajo
@app.route('/port/<input_port>/off', methods = ['PUT'])
def port_off(input_port):
    port = input_port.lower()
    if (not _check_port(port)):
        abort(404)
    
    
    GPIO.output(config.getint(port, 'gpio_pin'), False)
    return "Off"

# Toggle LED
@app.route('/port/<input_port>/toggle', methods = [ 'PUT' ])
def port_toggle(input_port):
    port = input_port.lower()
    if (not _check_port(port)):
        abort(404)
    
   
    GPIO.output(config.getint(port, 'gpio_pin'), not GPIO.input(config.getint(port, 'gpio_pin')))
    if(GPIO.input(config.getint(port, 'gpio_pin'))):
        return "On"
    else:
        return "Off"



# Funciones privadas
def _check_port(port):
    return port in allowed_ports


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
