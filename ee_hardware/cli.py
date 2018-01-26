import click

class sACNDeviceHardware():
    def __init__(self, num_leds):
        self._channel_prefix_single = 'p'
        self._device = 'sACNDevice'
        self._num_leds = num_leds
        self._color_per_led = 3
        self._channels = self._color_per_led * self._num_leds

    @property
    def hardware(self):
        out = f'[hardware]\n'
        out +=f'device = {self._device}\n'
        out +=f'channels = {self._channels}\n'
        return out

    @property
    def channels(self):
        out = f'[channels]\n'
        for ch in range(self._num_leds):
            r,g,b = [(ch)*3+i+1 for i in range(3)]
            out += f'{self._channel_prefix_single}{ch} = {r}, {g}, {b}\n'
        return out

@click.command()
@click.option('--num_leds','-n', default=8)
def ee_hardware(num_leds):
    d = sACNDeviceHardware(num_leds)
    click.echo(d.hardware)
    click.echo(d.channels)
