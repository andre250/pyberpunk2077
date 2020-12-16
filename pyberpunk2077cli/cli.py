import os
import click


class CLI(click.MultiCommand):
    def list_commands(self, ctx):
        apps = []
        apps_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "applications"))
        for filename in os.listdir(apps_dir):
            if filename.endswith(".py") and filename.startswith("app_"):
                apps.append(filename.replace("app_", "").replace(".py", ""))
        apps.sort()
        return apps

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"pyberpunk2077cli.applications.app_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=CLI)
def cli():
    """Initializing protocol Pyberpunk2077."""
    pass

# References:
#    - https://click.palletsprojects.com/en/7.x/advanced/
#    - https://click.palletsprojects.com/en/7.x/commands/
