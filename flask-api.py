from flask import Flask
from flask_httpauth import HTTPBasicAuth
import RPi.GPIO as GPIO
import time


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "usename": "pass",
}

def open_key(angle):
    GPIO.setmode(GPIO.BCM)

    gp_out = 2
    GPIO.setup(gp_out, GPIO.OUT)
    motor = GPIO.PWM(gp_out, 50)
    motor.start(0.0)

    motor.ChangeDutyCycle(angle)
    time.sleep(0.5)

    GPIO.cleanup()

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/open')
@auth.login_required
def open():
    open_key(7.2)
    print("open!")
    return "open"

@app.route("/close")
@auth.login_required
def close():
    open_key(2.5)
    print("close!")
    return "close"

if __name__ == '__main__':
    app.run(debug=True, host='192.168.3.5', port="port")
