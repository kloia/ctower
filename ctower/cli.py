import boto3
from typing import Optional
import typer
from rich.table import Table
from rich.panel import Panel
from functools import lru_cache
from rich.prompt import Confirm

from guardrail_identifiers import *
from utils import (
    get_boto_session,
    find_guardrail_control_by_id,
    get_organizational_units,
    get_rich_console,
    print_error_panel,
    print_success_panel,
    get_control_tower_client,
    find_organizational_unit_by_id_or_name,
    _list_enabled_controls,
)


session = get_boto_session()
console = get_rich_console()
ct_client = get_control_tower_client()
AWS_REGION_NAME = session.region_name


apply_app = typer.Typer(no_args_is_help=True)
remove_app = typer.Typer(no_args_is_help=True)
ls_app = typer.Typer(no_args_is_help=True)
controls_app = typer.Typer(no_args_is_help=True)
ls_app.add_typer(controls_app, name="controls")


def _print_list_of_guardrails(guardrail_list, header, do_print=True):
    table = Table(title=f"[bold]{header}", title_style="white on black")
    table.add_column(
        "[bold]ControlTower GuardRail Identifiers",
        justify="left",
        style="green",
        no_wrap=True,
    )
    table.add_column("[bold]Details", style="cyan")

    for gr in guardrail_list:
        table.add_row(f"[bold]{gr.get('id')}", f"{gr.get('text')}")
    if do_print:
        console.print(table)
    return table


@ls_app.command("enabled-controls")
def list_enabled_controls_for_organizational_unit(
    organizational_unit: str = typer.Option(
        ...,
        "--organizational-unit",
        "-ou",
        help="ID or Name of Organizational Unit to list its enabled controls. Try: `ls organizational-units` command",
    )
):
    # get details of the given organizational unit
    o_unit = find_organizational_unit_by_id_or_name(organizational_unit)
    if not o_unit:
        raise typer.Exit(
            "Please provide a correct Organizational Unit ID. Try: `ls organizational-units` command"
        )
    organizational_unit_arn = o_unit.get("Arn")
    organizational_unit_id = o_unit.get("Id")
    organizational_unit_name = o_unit.get("Name")

    enabled_controls = _list_enabled_controls(organizational_unit_arn)

    table = Table(
        title=f"[bold]Enabled GuardRail Controls for O.U. [blue]{organizational_unit_name}[/] ([green]{organizational_unit_id}[/])",
        title_style="white on black",
    )
    table.add_column("[bold]GuardRail Control Identifiers", justify="left")

    enabled_control_identifiers = [
        ec.get("controlIdentifier") for ec in enabled_controls
    ]
    for eci in enabled_control_identifiers:

        before, after = eci.rsplit("/", 1)

        table.add_row(f"[white]{before}/[bold][blue]{after}")
    console.print(table)


@ls_app.command("organizational-units")
def _list_ous():
    organizational_units = get_organizational_units()
    if not organizational_units:
        raise typer.Exit("No organizational units found!")

    table = Table(title=f"[bold]Organizational Units", title_style="white on black")
    table.add_column("[bold]Name", justify="left", style="green", no_wrap=True)
    table.add_column("[bold]Identifier", justify="center", style="white", no_wrap=True)
    table.add_column("[bold]ARN", justify="center", style="cyan", no_wrap=True)

    for ou in organizational_units:
        table.add_row(
            f"[bold]{ou.get('Name')}", f"[bold]{ou.get('Id')}", f"{ou.get('Arn')}"
        )

    console.print(table)


@apply_app.command("strongly-recommended")
def _apply_strongly_recommended_controls(
    organizational_unit: str = typer.Option(
        ...,
        "--organizational-unit",
        "-ou",
        help="ID or Name of Organizational Unit to apply GuardRail controls. Try: `ls organizational-units` command",
    )
):
    pass


@controls_app.command("all")
def _list_all_guardrails():
    _list_strongly_recommended_guardrails()
    _list_elective_guardrails()
    _list_data_residency_guardrails()


@controls_app.command("elective")
def _list_elective_guardrails():
    _print_list_of_guardrails(ELECTIVE_GUARDRAILS, "ELECTIVE GUARDRAILS")


@controls_app.command("data-residency")
def _list_data_residency_guardrails():
    _print_list_of_guardrails(DATA_RESIDENCY_GUARDRAILS, "DATA RESIDENCY GUARDRAILS")


@controls_app.command("strongly-recommended")
def _list_strongly_recommended_guardrails():
    _print_list_of_guardrails(
        STRONGLY_RECOMMENDED_GUARDRAILS, "STRONGLY RECOMMENDED GUARDRAILS"
    )


@apply_app.command("control")
def _list_all_guardrails(
    organizational_unit: str = typer.Option(
        ...,
        "--organizational-unit",
        "-ou",
        help="ID or Name of Organizational Unit to get the controls from.",
    ),
    control_id: str = typer.Option(
        ...,
        "--control-id",
        "-cid",
        help="Control Identifier. Try: `ls controls all` command",
    ),
):
    is_applied = _apply_control_to_organizational_unit(organizational_unit, control_id)


def _apply_control_to_organizational_unit(ou_name_or_id, control_id):
    control_dict = find_guardrail_control_by_id(control_id)
    if not control_dict:
        print_error_panel(
            f"Given Control ID: [blue][bold]{control_id}[/][/] is not found in the list. Try: [cyan]`ls controls all`[/] command"
        )
        raise typer.Exit()
    control_arn = generate_guardrail_arn(control_id, AWS_REGION_NAME)

    console.print(
        Panel(
            f"\n[bold]{control_dict.get('text')}\n",
            title=f"Selected Control: [blue][bold]{control_id}",
            title_align="left",
            subtitle=f"[cyan]{control_arn}[/]",
        )
    )

    found_ou = find_organizational_unit_by_id_or_name(ou_name_or_id)
    if not found_ou:
        print_error_panel(
            f"Given Organizational UNIT ID/NAME: [green][bold]{ou_name_or_id}[/][/] is not found. Try: [cyan]`ls organizational-units`[/] command"
        )
        raise typer.Exit()

    console.print(
        Panel(
            f"\nId: [bold][green]{found_ou.get('Id')}[/][/]\nName: [bold][green]{found_ou.get('Name')}[/][/]\n",
            title=f"Selected O.U.: [green][bold]{found_ou.get('Name')}",
            title_align="left",
            subtitle=f"[cyan]{found_ou.get('Arn')}[/]",
        )
    )

    found_ou_arn = found_ou.get("Arn")

    do_apply = Confirm.ask(
        f"\nAre you sure you want to enable [bold][blue]{control_id}[/][/] on [bold][green]{found_ou.get('Name')}[/][/]",
        console=console,
    )
    if not do_apply:
        console.print("Aborting apply...")
        raise typer.Abort()

    try:
        response = ct_client.enable_control(
            controlIdentifier=control_arn, targetIdentifier=found_ou_arn
        )
        operation_id = response.get("operationIdentifier", False)
        print_success_panel(
            f"\n[bold][green]Successfuly enabled[/] [bold][blue]{control_id}[/][/] on [bold][green]{found_ou.get('Name')}[/][/]"
        )
    # except ct_client.exceptions.ValidationException as e:
    # except ct_client.exceptions.ResourceNotFoundException as e:
    except Exception as e:
        print_error_panel(
            f"[bold]Failed to apply control [blue]{control_arn}[/] on [green]{found_ou_arn}[/].[/]\n\n[red]Exception:[/] {str(e)}"
        )
        typer.Exit()

    # operation_data = _get_control_operation(operation_id)
    # table = Table()
    # table.add_column(header="KEY", style="magenta")
    # table.add_column(header="VALUE", style="cyan")
    # for op_key, op_value in operation_data.items():
    #     table.add_row(f"[bold]{op_key}", f"{str(op_value)}")
    # console.print(Panel(table, f"sadasda") )
