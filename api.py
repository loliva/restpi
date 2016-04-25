#!/usr/bin/env python
import time
import ConfigParser
import RPi.GPIO as GPIO
import serial
from flask import Flask, jsonify, url_for, abort, make_response, request
GPIO.setwarnings(False)


# Configuracion Base
config = ConfigParser.RawConfigParser()
config.read('gpio.cfg')

# Defino puertos
allowed_ports = ['port1', 'port2', 'port3', 'port4', 'port5', 'port6']

# Seteo GPIO
GPIO.setmode(GPIO.BOARD)

# Defino el serial
s = serial.Serial('/dev/ttyACM0', 9600)

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

# Toggle 
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


# escribir un mensaje en arduino via serial
@app.route('/ard/<input_sport>', methods = [ 'PUT'])
def sport_in(input_sport):
    if input_sport == '1':
	s.write(input_sport)
	return "encendido"
    if input_sport == '0':
	s.write(input_sport)
	return "apagado"
    else:
	return "Valor no corresponde"


# leer un mensaje en arduino via serial
@app.route('/ard/read/<input_sread>', methods = [ 'GET'])
def sread_in(input_sread):
    if input_sread == 'all':
       i = 0
       while (1 < 4): 
	   time.sleep(1)
           msg = s.readline()
           return msg
#           s.flush()
       i = i + 1

    else:
        return "No existen valores"



# Funciones privadas
def _check_port(port):
    return port in allowed_ports


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
