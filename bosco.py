from subprocess import run
from multiprocessing import Process
from gpiozero import AngularServo
from neopixel import NeoPixel
from board import D21
import time
import random

left_arm = None
right_arm = None
head = None
lights = None

def init():
    global left_arm, right_arm, head, lights
    left_arm = AngularServo(17, min_angle = 90, max_angle = -90)
    right_arm = AngularServo(27)
    head = AngularServo(22)
    lights = NeoPixel(D21, 8)
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

def wait():
    input()

def sting():
    p = Process(
        target = run, 
        args = ['ogg123 sting.ogg'.split(' ')], 
        kwargs = {'capture_output':True},
        )
    p.start()
    return p

def espeak(str,
        wpm = 175, 
        voice = 'en-us', 
        pitch = 50,
        amplitude = 100,
        whisper = False, 
        croak = False):
    if whisper:
        voice += '+whisper'
    if croak:
        voice += '+croak'
    command = f'espeak-ng -v{voice} -s{wpm} -p{pitch} -a{amplitude}'
    return run(command.split()+[str])

def say(str):
    p = Process(target = espeak, args = [str], kwargs = {'wpm':150})
    p.start()
    return p

def blink(duration):
    def offon():
        lights[6:] = [(0,0,0)]*2
        time.sleep(duration)
        lights[6:] = [(255,255,255)]*2
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
        nonlocal servo
        while time.time() <= end_time:
            servo.value = (
                start_position 
                + distance * path(
                    (time.time()-start_time)/duration
                    )
                )
            print(servo.value)
            time.sleep(0.050)
            #servo expects updates every 20ms, so no sense in waiting shorter.
        servo.value = destination
        time.sleep(0.050)
        servo.value = None
    
    p = Process(target = go)
    p.start()
    return p
    
#should map 0 -> 0 and 1 -> 1 and be continuous
servo_paths = {
    'linear': (lambda x: x),
    'quadratic': (lambda x: x**2/2 if x <= 0.5 else 1-(1-x)**2/2),
    'cubic': (lambda x: (3 - 2*x) * x**2),
}

def fidget():
    def go():
        while True:
            servo = random.choice([left_arm, right_arm, head])
            movetime = random.uniform(2,4)
            moveplace = random.triangular(-1,1,0)
            waittime = random.uniform(5,10)
            m = move(servo, moveplace, movetime, path='quadratic')
            m.join()
            time.sleep(waittime)
    p = Process(target = go)
    p.start()
    return p

def cylon(color, period = 1/6):
    def go():
        direction = 1
        position = 0
        while True:
            lights[position] = 0
            position += direction
            lights[position] = color
            if position in [0,5]:
                direction = -direction
            time.sleep(period)
    p = Process(target = go)
    p.start()
    return p

if __name__ == '__main__':
    init()
    test()
    disconnect_peripherals()