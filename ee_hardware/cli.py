import click

class sACNDeviceHardware():
    def __init__(self, num_leds):
        self.device = 'sACNDevice'
        self.num_leds = 1
        self.color_per_led = 3
        self.channels = self.color_per_led*self.num_leds

    @property
    def hardware(self):
        s_name = 'hardware'
        out = f'[{s_name}]\n'
        out +=f'device = {self.device}\n'
        out +=f'channels = {self.channels}\n'
        return out

@click.command()
@click.option('--num_leds','-n', default=1)
def ee_hardware(num_leds):
    d = sACNDeviceHardware(num_leds)
    click.echo(d.hardware)
