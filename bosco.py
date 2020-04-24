from subprocess import run
from multiprocessing import Process
from gpiozero import AngularServo
from neopixel import NeoPixel
from board import D18
import time

def init():
    global left_arm = AngularServo(10, min_angle = 90, max_angle = -90)
    global right_arm = AngularServo(11)
    global head = AngularServo(12)
    global lights = NeoPixel(D18, 8)
    global mouth = lights[:6]
    global eyes = lights[6:]
    lights.fill((255,0,0))

def disconnect_peripherals():
    for servo in (left_arm, right_arm, head):
        servo.value = None
    lights.deinit()

def test():
    b = blink()
    s = sting()
    pp = [move(servo, 0.5,2,'linear') for servo in (left_arm, right_arm, head)]+[b,s]
    [p.join() for p in pp]
    pp = [move(servo, 0, 1, 'quadratic') for servo in (left_arm, right_arm, head)]
    [p.join() for p in pp]
    espeak('hello world!')

def sting():
    p = Process(target = run, args = ['aplay','sting.ogg'])
    p.start()
    return p

def espeak(str, args = ['-ven-us']):
    p = Process(target = run, args = [['espeak-ng']+args+[str]])
    p.start()
    return p

def blink(duration):
    def offon():
        eyes.fill((0,0,0))
        time.sleep(duration)
        eyes.fill((255,255,255))
    p = Process(target = offon)
    p.start()
    return p

def move(servo, destination, duration, path='linear')
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