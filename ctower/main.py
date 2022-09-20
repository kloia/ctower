import typer
from rich.traceback import install
from guardrail_identifiers import *
import cli
from utils import *

install(show_locals=True)



session = get_boto_session()
console = get_rich_console()
ct_client = get_control_tower_client()
AWS_REGION_NAME = session.region_name
typer.Typer()
app = typer.Typer(no_args_is_help=True)
app.add_typer(cli.apply_app, name="apply")
app.add_typer(cli.remove_app, name="remove")
app.add_typer(cli.ls_app, name="ls")




def print_boto_region_and_profile():
    profile = session.profile_name
    region = session.region_name
    result = f"--region: [bold]{region}[/]"
    if profile:
        result = f"--profile: [bold]{profile}[/] | " + result
    result = f"awscli: " + result

    console.print(result, style="blue on white", justify="center")


@app.command("sync")
def _sync_organizational_unit_controls(
    from_organizational_unit: str = typer.Option(
        ...,
        "--from-organizational-unit",
        "-fou",
        help="ID or Name of Organizational Unit to get the controls from.",
    ),
    to_organizational_unit: str = typer.Option(
        ...,
        "--to-organizational-unit",
        "-tou",
        help="ID or Name of Organizational Unit to apply GuardRail controls to.",
    ),
    # to_organizational_unit: str = typer.Option(
    #     ...,
    #     "--to-organizational-unit",
    #     "-tou",
    #     help="ID or Name of Organizational Unit to apply GuardRail controls to.",
    # ),
):

    pass

def run_app():
    sanity_checks()
    console.print()
    console.print("kloia/ctower v.0.1", style="blue on white", justify="center")
    print_boto_region_and_profile()
    console.print()
    app()


if __name__ == "__main__":
    run_app()
    
    

"""

"""