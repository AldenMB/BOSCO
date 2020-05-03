from gpiozero import DigitalOutputDevice, OutputDevice


class CountDisplay:
    def __init__(self, reset_pin, increment_pin, change_time=0, background=True):
        self._reset_pin = OutputDevice(reset_pin)
        self._increment_pin = DigitalOutputDevice(increment_pin)
        self.change_time = change_time
        self.background = background
        self.reset()

    def reset(self):
        self._reset_pin.on()
        self._reset_pin.off()
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newval):
        if newval < 0:
            raise ValueError("CountDisplay cannot show negative numbers.")
        if newval > self.value:
            self._increment_pin.blink(
                on_time=self.change_time / 2,
                off_time=self.change_time / 2,
                n=newval - self.value,
                background=self.background,
            )
        elif newval < self.value:
            self.reset()
            self._increment_pin.blink(
                on_time=self.change_time / 2,
                off_time=self.change_time / 2,
                n=newval,
                background=self.background,
            )
        self._value = newval
