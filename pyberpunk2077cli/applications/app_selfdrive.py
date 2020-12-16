import click
import time
import keyboard
from pyberpunk2077cli.env import *
from pyberpunk2077cli.source import src_selfdrive

class Context:
    def __init__(self):
        self.selfdrive = src_selfdrive.Delamain()


@click.group()
@click.pass_context
def cli(ctx):
    """Cyberpunk 2077 self driving"""
    ctx.obj = Context()


@cli.command()
@click.option("-t", "--test", type=bool, help="Set True if you want to go Test-Mode, leave to go on Self-Drive.", default=False)
@click.pass_context
def run(ctx, test, mode_name="Self-Drive"):
    last_mili = time.time()
    mode = test
    if mode: mode_name = "Test-Mode"
    for i in range(START_IN, 1, -1):
        click.echo('Starting engines in {}: {} seconds'.format(mode_name, i))
        time.sleep(1)
    while True:
        if keyboard.is_pressed('p'):
            click.pause()
        click.echo('Elapsed time to frame in {}: {} seconds'.format(mode_name, time.time() - last_mili))
        last_mili = time.time()
        lane_1, lane_2 = ctx.obj.selfdrive.start(mode=mode)
        if not mode:
            if lane_1 < 0 and lane_2 < 0:
                click.echo("Turning right")
                ctx.obj.selfdrive.right()
            elif lane_1 > 0 and lane_2 > 0:
                click.echo("Turning left")
                ctx.obj.selfdrive.left()
            else:
                click.echo("Keep straight, jesus!")
                ctx.obj.selfdrive.front()

        if ctx.obj.selfdrive.check_stop():
            break

# References:
#   - https://click.palletsprojects.com/en/7.x/complex/
