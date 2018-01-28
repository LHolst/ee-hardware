import click
from colour import Color

from enum import Enum


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
    def __init__(self, num_leds, universe=1, channels=512, channel_offset=0):
        self._channel_prefix_single = 'p'
        self._device = 'sACNDevice'
        self._num_leds = num_leds
        self._universe = universe
        self._color_per_led = 3
        self._channels = channels
        self._channel_offset = channel_offset

    @property
    def hardware(self):
        out = f'[hardware]\n'
        out +=f'device = {self._device}\n'
        out +=f'universe = {self._universe}\n'
        out +=f'channels = {self._channels}\n'
        return out

    def channel_name(self, ch):
        return f'{self._channel_prefix_single}{ch}_u{self._universe}'

    @property
    def channels(self):
        out = f'[channels]\n'
        for ch in range(self._num_leds):
            r,g,b = [(ch)*3+i+1+self._channel_offset for i in range(3)]
            out += f'{self.channel_name(ch+self._channel_offset)} = {r}, {g}, {b}\n'
        return out


    def state(self, condition, offset, num_leds, e_params):
        out = ''

        for ch in range(int(num_leds)):
            out += f'[state]\n'
            out += f'condition = {condition}\n'
            out += f'target = {self.channel_name(ch+offset+self._channel_offset)}\n'
            for k, v in e_params.items():
                if isinstance(v, (list,tuple)):
                    v = ','.join(f'{x:.2f}' for x in v)
                out += f'{k} = {v}\n'
        return out

    def event(self, trigger, offset, num_leds, value, runtime):
        v = ','.join(str(x) for x in value.rgb)
        runtime = '0.6'
        out = ''
        for ch in range(int(num_leds)):
            out += f'[event]\n'
            out += f'trigger = {trigger}\n'
            out += f'target = {self.channel_name(ch+offset+self._channel_offset)}\n'
            out += f'value = {v}\n'
            out += f'runtime = {runtime}\n'
        return out


@click.command()
def ee_hardware():
    d1 = sACNDeviceHardware(170, universe=1)
    d2 = sACNDeviceHardware(130, universe=2, channel_offset=512)
    click.echo(d1.hardware)
    click.echo(d2.hardware)
    click.echo(d1.channels)
    click.echo(d2.channels)


    o1, l1 = 0, 170
    o2, l2 = 0, 130
    static_effect_hasNoShip = static(Color('limegreen',luminance=0.2))
    static_effect_jumped = static(Color('white'))
    static_effect_notInNebula = static(Color(rgb=(13/255.0, 38/255.0, 38/255.0)))
    glow_effect_InNebula = glow(Color('blueviolet'), Color('limegreen'), 2.0)
    glow_effect_RedAlert = glow(Color('red'), Color('black'), 1.0)
    glow_effect_YellowAlert = glow(Color('yellow'), Color('black'), 1.0)
    click.echo(d1.state(f'HasShip == 0', o1, l1, static_effect_hasNoShip))
    click.echo(d2.state(f'HasShip == 0', o2, l2, static_effect_hasNoShip))
    click.echo(d1.state(f'InNebula == 0', o1, l1, static_effect_notInNebula))
    click.echo(d2.state(f'InNebula == 0', o2, l2, static_effect_notInNebula))
    click.echo(d1.state(f'InNebula', o1, l1, glow_effect_InNebula))
    click.echo(d2.state(f'InNebula', o2, l2, glow_effect_InNebula))
    click.echo(d1.state(f'Jumped', o1, l1, static_effect_jumped))
    click.echo(d2.state(f'Jumped', o2, l2, static_effect_jumped))

    click.echo(d1.state(f'RedAlert', 30, 10, glow_effect_RedAlert))
    click.echo(d1.state(f'RedAlert', 100, 10, glow_effect_RedAlert))
    click.echo(d2.state(f'RedAlert', 30, 10, glow_effect_RedAlert))
    click.echo(d2.state(f'RedAlert', 70, 10, glow_effect_RedAlert))
    click.echo(d1.state(f'YellowAlert', 30, 10, glow_effect_YellowAlert))
    click.echo(d1.state(f'YellowAlert', 100, 10, glow_effect_YellowAlert))
    click.echo(d2.state(f'YellowAlert', 30, 10, glow_effect_YellowAlert))
    click.echo(d2.state(f'YellowAlert', 70, 10, glow_effect_YellowAlert))

    click.echo(d1.event('<RearShield', o1, l1, Color('orange'), 0.5))
    click.echo(d1.event('<FrontShield', o1, l1, Color('orange'), 0.5))
    click.echo(d1.event('<Hull', o1, l1, Color('red'), 0.5))
    click.echo(d2.event('<RearShield', o2, l2, Color('orange'), 0.5))
    click.echo(d2.event('<FrontShield', o2, l2, Color('orange'), 0.5))
    click.echo(d2.event('<Hull', o2, l2, Color('red'), 0.5))

