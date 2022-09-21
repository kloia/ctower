import typer
from rich.traceback import install
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from itertools import zip_longest
from . import guardrail_identifiers
from . import cli
from . import utilities
from rich.terminal_theme import MONOKAI
import os
install(show_locals=True)
from rich.console import Group


session = utilities.get_boto_session()
console = utilities.get_rich_console()
ct_client = utilities.get_control_tower_client()
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

def check_control_tower_available_on_region():
    available_services = session.get_available_services()
    return "controltower" in available_services

def sanity_checks():
    if not check_control_tower_available_on_region():
        console.print(
            Panel(
                f"[bold]Control Tower is not enabled on the {AWS_REGION_NAME}. Aborting...",
                title="[red][bold]ERROR",
                title_align="center",
                expand=True,
            )
        )
        raise typer.Exit()
    



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
    """Syncs GuardRail Controls from an Organizational Unit to another Organizational Unit"""
    from_ou = utilities.find_organizational_unit_by_id_or_name(from_organizational_unit)
    if not from_ou:
        utilities.print_error_panel("Please provide a correct Organizational Unit ID for [blue]`--from-organizational-unit`[/]. Try: `ls organizational-units` command")
        raise typer.Exit()
    to_ou = utilities.find_organizational_unit_by_id_or_name(to_organizational_unit)
    if not to_ou:
        utilities.print_error_panel("Please provide a correct Organizational Unit ID for [blue]`--to-organizational-unit`[/]. Try: `ls organizational-units` command")
        raise typer.Exit()



    from_ou_enabled_control_identifiers = utilities._list_enabled_controls(from_ou.get("Arn"))
    to_ou_enabled_control_identifiers = utilities._list_enabled_controls(to_ou.get("Arn"))
    
    from_ou_enabled_control_ids = [utilities.get_control_id_from_control_identifier(c_identifier) for c_identifier in from_ou_enabled_control_identifiers]
    to_ou_enabled_control_ids = [utilities.get_control_id_from_control_identifier(c_identifier) for c_identifier in to_ou_enabled_control_identifiers]
    mandatory_control_ids = [_.get('id') for _ in guardrail_identifiers.MANDATORY_CONTROL_TOWER_GUARDRAILS]
    # remove the mandatory controls, as the control tower api has no permission to enable/disable them
    only_on_from_ou = list(set(from_ou_enabled_control_ids) - set(to_ou_enabled_control_ids) - set(mandatory_control_ids))
    only_on_to_ou= list(set(to_ou_enabled_control_ids) - set(from_ou_enabled_control_ids) - set(mandatory_control_ids))

    # console.print(only_on_from_ou)
    # console.print(only_on_to_ou)
    # console.print('-'*20)

    
    unique_controls_zip = list(zip_longest(sorted(only_on_from_ou), sorted(only_on_to_ou), fillvalue=''))
    
    # prompt
    # table = Table(title=f"Unique Controls on Organizational Units", title_style="",)
    table = Table()
    table.add_column(f"Controls that are only on [blue]{from_ou.get('Name')}",justify="left",)
    table.add_column(f"Controls that are only on [green]{to_ou.get('Name')}",justify="left",)
    
    for from_, to_ in unique_controls_zip:
        str_from_ = f"[bold][blue]+ {from_}" if from_ else ''
        str_to = f"[bold][green]+ {to_}" if to_ else ''
        table.add_row(str_from_, str_to)
    
    _to_apply_control_panels = []
    for control_id in only_on_from_ou:
        control_dict = utilities.find_guardrail_control_by_id(control_id)
        if not control_dict:
            utilities.print_error_panel(
                f"Given Control ID: [blue][bold]{control_id}[/][/] is not found in the list. Try: [cyan]`ls controls all`[/] command"
            )
            continue

        control_arn = guardrail_identifiers.generate_guardrail_arn(control_id, AWS_REGION_NAME)
        control_panel = Panel(
            f"\n[bold]{control_dict.get('text')}\n",
            title=f"Selected Control: [blue][bold]{control_id}",
            title_align="left",
            subtitle=f"[cyan]{control_arn}[/]",
        )
        _to_apply_control_panels.append(control_panel)
        _to_apply_control_panels.append('')
    
    if not only_on_from_ou:
        console.print(table)
        utilities.print_error_panel(f"There are [bold][red]no GuardRail Controls to apply.[/][/] [blue]O.U. {from_ou.get('Name')}[/] has no unique Controls when compared to [green]O.U. {to_ou.get('Name')}[/]. No changes are made.")
        raise typer.Exit()
    
    
    to_be_applied_panel_group = Group(table, f"", Panel(Group(*_to_apply_control_panels), title_align='left', title=f"[bold]Controls will be applied to [green]{to_ou.get('Name')}[/]"))
    console.print(Panel(to_be_applied_panel_group, title=f"[bold]SYNC Controls Operation from [blue]{from_ou.get('Name')}[/] to [green]{to_ou.get('Name')}[/]"))
    
    
    do_apply = Confirm.ask(
        f"\nAre you sure you want to [bold][green]add[/][/] [bold][blue]{len(only_on_from_ou)}[/][/] Controls to [bold][green]{to_ou.get('Name')}[/][/]",
        console=console,
        
    )
    if not do_apply:
        raise typer.Abort()
    cli._apply_list_of_controls_to_organizational_unit(to_ou.get('Name'), only_on_from_ou)
    
def run_app():
    sanity_checks()
    console.print()
    console.print("kloia/ctower v.0.1", style="blue on white", justify="center")
    print_boto_region_and_profile()
    console.print()
    try:
        app()
    except Exception as e:
        utilities.print_error_panel(str(e))
    finally:
        console.save_svg("output.svg", theme=MONOKAI)

if __name__ == "__main__":
    run_app()