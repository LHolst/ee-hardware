import click
from colour import Color
import math
import random


def static(value):
    return {
        'value': value.rgb
        }

def glow(min_value, max_value, time):
    return {
        'effect': 'glow',
        'min_value': min_value.rgb,
        'max_value': max_value.rgb,
        'time': time
        }

def blink(on_time, off_time):
    return {
        'effect': 'blink',
        'on_time': on_time,
        'off_time': off_time
        }

def variable(inputs, min_input, max_input, min_output, max_output):
    return {
        'effect': 'variable',
        'input': inputs,
        'min_input': min_input,
        'max_input': max_input,
        'min_output': min_output,
        'max_output': max_output
        }



class sACNDeviceHardware():
    def __init__(self, num_leds, start_universe=1, universe_boundary=510, channels=512):
        self._channel_prefix_single = 'p'
        self._device = 'sACNDevice'
        self._num_leds = num_leds
        self._universe = start_universe
        self._universe_boundary = universe_boundary
        self._color_per_led = 3
        self._channels = channels
        self._states = []
        self._events = []

    @property
    def hardware(self):
        out = ''
        num_universes = math.ceil(self._num_leds*self._color_per_led/self._universe_boundary)
        for u in range(num_universes):
            out += f'[hardware]\n'
            out +=f'device = {self._device}\n'
            out +=f'universe = {self._universe+u}\n'
            out +=f'channels = {self._channels}\n'
        return out

    def channel_name(self, led):
        universe_offset = math.floor(led*self._color_per_led/self._universe_boundary)
        return f'{self._channel_prefix_single}{led}_u{self._universe+universe_offset}'

    @property
    def channels(self):
        out = f'[channels]\n'
        for led in range(self._num_leds):
            universe_offset = math.floor(led*self._color_per_led/self._universe_boundary)
            boundary_offset = universe_offset*(self._channels - self._universe_boundary)
            r,g,b = [(led)*self._color_per_led+boundary_offset+i+1 for i in range(self._color_per_led)]
            out += f'{self.channel_name(led)} = {r}, {g}, {b}\n'
        return out

    @property
    def states(self):
        return ''.join(self._states)

    @property
    def events(self):
        return ''.join(self._events)


    def addState(self, condition, offset, num_leds, e_params):
        out = ''

        for ch in range(int(num_leds)):
            out += f'[state]\n'
            out += f'condition = {condition}\n'
            out += f'target = {self.channel_name(ch+offset)}\n'
            for k, v in e_params.items():
                if isinstance(v, (list,tuple)):
                    v = ','.join(f'{x:.2f}' for x in v)
                out += f'{k} = {v}\n'
        self._states.append(out)

    def addEvent(self, trigger, offset, num_leds, value, runtime):
        v = ','.join(str(x) for x in value.rgb)
        runtime = '0.6'
        out = ''
        for ch in range(int(num_leds)):
            out += f'[event]\n'
            out += f'trigger = {trigger}\n'
            out += f'target = {self.channel_name(ch+offset)}\n'
            out += f'value = {v}\n'
            out += f'runtime = {runtime}\n'
        self._events.append(out)



def buildDevice(device):
    click.echo(device.hardware)
    click.echo(device.channels)
    click.echo(device.states)
    click.echo(device.events)


@click.command()
def ee_hardware():
    device = sACNDeviceHardware(300, start_universe=1)
    offset, led_count = 0, 300

    static_effect_hasNoShip = static(Color('limegreen',luminance=0.2))
    static_effect_jumped = static(Color('white'))
    static_effect_notInNebula = static(Color(rgb=(13/255.0, 38/255.0, 38/255.0)))
    device.addState('HasShip == 0', offset, led_count, static_effect_hasNoShip)
    device.addState('InNebula == 0', offset, led_count, static_effect_notInNebula)
    device.addState('Jumped', offset, led_count, static_effect_jumped)

    for i in range(0,300,15):
        glow_effect_InNebula = glow(Color('blueviolet'), Color('limegreen'), random.uniform(1.8,2.2))
        device.addState('InNebula', i, 15, glow_effect_InNebula)

    glow_effect_RedAlert = glow(Color('red'), Color('black'), 1.0)
    for i in range(0,300,10):
        device.addState('RedAlert', i, 5, glow_effect_RedAlert)

    glow_effect_YellowAlert = glow(Color('yellow'), Color('black'), 1.0)
    for i in range(5,300,10):
        device.addState('YellowAlert', i, 5, glow_effect_YellowAlert)

    device.addEvent('<RearShield', offset, led_count, Color('orange'), 0.5)
    device.addEvent('<FrontShield', offset, led_count, Color('orange'), 0.5)
    device.addEvent('<Hull', offset, led_count, Color('red'), 0.5)

    buildDevice(device)