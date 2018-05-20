# Code to be running on the Minibot in order to receive commands
# Runs on Python 3

import RPi.GPIO as GPIO
import signal
import sys
import time
import threading
import tornado.ioloop
import tornado.web

GPIO.setmode(GPIO.BCM)

PORT = 8080
PIN_INH = 27
PIN_IN1 = 18
PIN_IN2 = 17
PIN_IN3 = 13
PIN_IN4 = 6

left_pwm = None
right_pwm = None

def setup_motors():
  global left_pwm, right_pwm

  GPIO.setup(PIN_INH, GPIO.OUT)
  GPIO.setup(PIN_IN1, GPIO.OUT)
  GPIO.setup(PIN_IN2, GPIO.OUT)
  GPIO.setup(PIN_IN3, GPIO.OUT)
  GPIO.setup(PIN_IN4, GPIO.OUT)

  GPIO.output(PIN_INH, GPIO.HIGH)
  left_pwm = GPIO.PWM(PIN_IN1, 100)
  right_pwm = GPIO.PWM(PIN_IN3, 100)

  left_pwm.start(0)
  GPIO.output(PIN_IN2, GPIO.HIGH)
  right_pwm.start(0)
  GPIO.output(PIN_IN4, GPIO.HIGH)

def cleanup_motors():
  global left_pwm, right_pwm

  left_pwm.stop()
  right_pwm.stop()

  GPIO.cleanup()

def test_motors():
  print("l0 r0")
  set_motors(0, 0)
  time.sleep(1)

  print("l50 r0")
  set_motors(50, 0)
  time.sleep(1)

  print("l-50 r0")
  set_motors(-50, 0)
  time.sleep(1)

  print("l0 r50")
  set_motors(0, 50)
  time.sleep(1)

  print("l0 r-50")
  set_motors(0, -50)
  time.sleep(1)

  print("l0 r0")
  set_motors(0, 0)

def set_motors(l, r):
  global left_pwm, right_pwm

  if l < -100 or l > 100 or r < -100 or r > 100:
    return

  if l < 0:
    GPIO.output(PIN_IN2, GPIO.LOW)
    l = 100 + l
  else:
    GPIO.output(PIN_IN2, GPIO.HIGH)

  left_pwm.ChangeDutyCycle(l)

  if r < 0:
    GPIO.output(PIN_IN4, GPIO.LOW)
    r = 100 + r
  else:
    GPIO.output(PIN_IN4, GPIO.HIGH)

  right_pwm.ChangeDutyCycle(r)


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hi this is WallBot")

def execute_script(lines):
  for line in lines:
    parts = line.split(b" ")
    print("EXEC")
    print(parts)
    if b"forward" in parts[0]:
      speed = int(parts[1]) if len(parts) > 1 else 50
      set_motors(speed, speed)
    elif b"backward" in parts[0]:
      speed = int(parts[1]) if len(parts) > 1 else 50
      set_motors(-speed, -speed)
    elif b"counter_clockwise" in parts[0]:
      speed = int(parts[1]) if len(parts) > 1 else 50
      set_motors(-speed, speed)
    elif b"clockwise" in parts[0]:
      speed = int(parts[1]) if len(parts) > 1 else 50
      set_motors(speed, -speed)
    elif b"wait" in parts[0] and len(parts) > 1:
      time.sleep(float(parts[1]))
    elif b"stop" in parts[0]:
      set_motors(0, 0)

  print("DONE")
  set_motors(0, 0)

class ScriptHandler(tornado.web.RequestHandler):
  def post(self):
    data = self.request.body
    print("GOT")
    lines = data.split(b"\n")
    print(lines)
    if len(lines) > 0:
      self.write("OK")

      threading.Thread(
        target=execute_script,
        args=[lines]
      ).start()

    else:
      self.write("NO")


def signal_handler(signal, frame):
  print("STOP")
  cleanup_motors()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
  setup_motors()

  #test_motors()

  app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/script", ScriptHandler),
  ])
  #http_server = tornado.httpserver.HTTPServer(app)
  #http_server.listen(8080)
  app.listen(PORT)
  print("START")
  tornado.ioloop.IOLoop.current().start()
