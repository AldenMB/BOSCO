from subprocess import run
from multiprocessing import Process
from gpiozero import AngularServo
from neopixel import NeoPixel
from board import D18
import time

left_arm = None
right_arm = None
head = None
lights = None

def init():
    global left_arm, right_arm, head, lights, mouth, eyes
    left_arm = AngularServo(10, min_angle = 90, max_angle = -90)
    right_arm = AngularServo(11)
    head = AngularServo(12)
    lights = NeoPixel(D18, 8)
    lights.fill((255,0,0))

def disconnect_peripherals():
    for servo in (left_arm, right_arm, head):
        servo.value = None
    lights.deinit()

def test():
    b = blink(1.0)
    s = sting()
    pp = [move(servo, 0.5,2,'linear') for servo in (left_arm, right_arm, head)]+[b,s]
    [p.join() for p in pp]
    pp = [move(servo, 0, 1, 'quadratic') for servo in (left_arm, right_arm, head)]
    [p.join() for p in pp]
    espeak('hello world!')

def sting():
    p = Process(target = run, args = ['cvlc sting.ogg --play-and-exit'.split(' ')])
    p.start()
    return p

def espeak(str, args = ['-ven-us']):
    p = Process(target = run, args = [['espeak-ng']+args+[str]])
    p.start()
    return p

def blink(duration):
    def offon():
        lights[6:].fill((0,0,0))
        time.sleep(duration)
        lights[6:].fill((255,255,255))
    p = Process(target = offon)
    p.start()
    return p

def move(servo, destination, duration, path='linear'):
    if path in servo_paths:
        path = servo_paths[path]
    
    start_time = time.time()
    end_time = start_time + duration
    
    start_position = servo.value
    distance = destination - start_position
    
    def go():
        while time.time() <= end_time:
            servo.value = (
                start_position 
                + distance * path(
                    (time.time()-start_time)/duration
                    )
                )
            time.sleep(0.010)
            #servo expects updates every 20ms, so no sense in waiting shorter.
        servo.value = destination
    
    p = Process(target = go)
    p.start()
    return p
    
#should map 0 -> 0 and 1 -> 1 and be continuous
servo_paths = {
    'linear': (lambda x: x),
    'quadratic': (lambda x: x**2/2 if x <= 0.5 else 1-(1-x)**2/2),
    'cubic': (lambda x: (3 - 2*x) * x**2),
}

if __name__ == '__main__':
    init()
    test()
    disconnect_peripherals()