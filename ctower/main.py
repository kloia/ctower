import boto3
from typing import Optional
import typer
import json
from termcolor import colored
from guardrail_identifiers import *
from tabulate import tabulate
import os 
from rich.console import Console
from rich.table import Table

console = Console()

def _create_boto_session():
    profile_name = os.environ.get('AWS_PROFILE', False)
    region_name = os.environ.get('AWS_REGION', False)
    _kwargs_dict = {}
    if profile_name:
        _kwargs_dict['profile_name']=profile_name
    if region_name:
        _kwargs_dict['region_name']=region_name
    session = boto3.session.Session(**_kwargs_dict)
    return session 

session = _create_boto_session()
AWS_REGION_NAME = session.region_name
ct_client = session.client("controltower")
typer.Typer()
app = typer.Typer(no_args_is_help=True)
apply_app = typer.Typer(no_args_is_help=True)
app.add_typer(apply_app, name="apply")
remove_app = typer.Typer(no_args_is_help=True)
app.add_typer(remove_app, name="remove")
ls_app = typer.Typer(no_args_is_help=True)
app.add_typer(ls_app, name="ls")
controls_app = typer.Typer(no_args_is_help=True)
ls_app.add_typer(controls_app, name="controls")


def list_roots():
    client = session.client("organizations")
    response = call_boto3_function(client, "list_roots")
    # print(json.dumps(response, indent=2, default=str))
    return response.get("Roots", False)


def list_accounts():
    client = session.client("organizations")
    response = call_boto3_function(client, "list_accounts")
    # print(json.dumps(response, indent=2, default=str))
    return response.get("Accounts", False)


def list_root_ids():
    return [root.get("Id") for root in list_roots()]


def call_boto3_function(client, function_name, kwargs=None):
    function_obj = getattr(client, function_name, False)
    if not function_obj and callable(function_obj):
        return False
    result = False
    if kwargs is not None:
        result = function_obj(**kwargs)
    else:
        result = function_obj()
    # TODO: pagination with NextToken
    result.pop("ResponseMetadata")
    return result


def get_current_organization():
    client = session.client("organizations")
    response = call_boto3_function(client, "describe_organization")
    # print(json.dumps(response, indent=2, default=str))
    return response.get("Organization", False)


def get_organizational_units():
    client = session.client("organizations")
    root_ids = list_root_ids()
    if not root_ids:
        raise typer.Exit("Failed to get Root ID for the Organization")

    organizational_units = []
    for root_id in root_ids:
        response = call_boto3_function(
            client, "list_organizational_units_for_parent", kwargs={"ParentId": root_id}
        )
        ous = response.get("OrganizationalUnits", False)
        if ous:
            organizational_units.extend(ous)
    return organizational_units


def _make_header(header):
    padding = "~" * 10
    return colored("{}{:^30s}{}".format(padding, header, padding), "yellow")


def _list_enabled_controls(organizational_unit_arn):
    try:
        response = call_boto3_function(
            ct_client,
            "list_enabled_controls",
            kwargs={"targetIdentifier": organizational_unit_arn},
        )
        return response.get("enabledControls", [])
    except ct_client.exceptions.ResourceNotFoundException as e:
        raise typer.Exit(
            f"Failed to list enabled controls on {organizational_unit_arn=}. \n\nException: {str(e)}"
        )


def _print_list_of_guardrails(guardrail_list, header, do_print=True):
    table = Table(title=f"[bold]{header}", title_style='white on black')
    table.add_column("[bold]ControlTower GuardRail Identifiers", justify="left", style="green", no_wrap=True)
    table.add_column("[bold]Details", style="cyan")

    for gr in guardrail_list:
        table.add_row(f"[bold]{gr.get('id')}", f"{gr.get('text')}")
    if do_print:
        console.print(table)
    return table


def find_organizational_unit_by_id_or_name(id_or_name: str):
    o_units = get_organizational_units()
    for o_u in o_units:
        if o_u.get("Id") == id_or_name or o_u.get("Name") == id_or_name:
            return o_u
    return False


def check_control_tower_available_on_region():
    available_services = session.get_available_services()
    return "controltower" in available_services


def sanity_checks():
    if not check_control_tower_available_on_region():
        raise typer.Exit(
            f"Control Tower is not enabled on the {AWS_REGION_NAME}. Aborting..."
        )


@ls_app.command("enabled-controls")
def list_enabled_controls_for_organizational_unit(
    organizational_unit: str = typer.Option(
        ..., '--organizational-unit','-ou',
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

    table = Table(title=f"[bold]Enabled GuardRail Controls for O.U. {organizational_unit_name} ({organizational_unit_id})", title_style='white on black')
    table.add_column("[bold]GuardRail Control Identifiers", justify="left")


    enabled_control_identifiers = [
        ec.get("controlIdentifier") for ec in enabled_controls
    ]
    for eci in enabled_control_identifiers:
        
        before, after = eci.rsplit('/', 1)
        
        table.add_row(f"[white]{before}/[bold][blue]{after}")
    console.print(table)

@ls_app.command("organizational-units")
def _list_ous():
    organizational_units = get_organizational_units()
    if not organizational_units:
        raise typer.Exit("No organizational units found!")
    
    table = Table(title=f"[bold]Organizational Units", title_style='white on black')
    table.add_column("[bold]Name", justify="left", style="green", no_wrap=True)
    table.add_column("[bold]Identifier", justify="center", style="white", no_wrap=True)
    table.add_column("[bold]ARN", justify="center", style="cyan", no_wrap=True)

    for ou in organizational_units:
        table.add_row(f"[bold]{ou.get('Name')}", f"[bold]{ou.get('Id')}", f"{ou.get('Arn')}")

    console.print(table)

@apply_app.command("strongly-recommended")
def _apply_strongly_recommended_controls(
    organizational_unit: str = typer.Option(
        ...,'--organizational-unit', '-ou',
        help="ID or Name of Organizational Unit to apply GuardRail controls. Try: `ls organizational-units` command",
    )
):
    pass


@apply_app.command("control")
def _list_all_guardrails(
    organizational_unit: str = typer.Option(
        ..., '--organizational-unit','-ou', help="ID or Name of Organizational Unit to get the controls from."
    ),
    control_id: str = typer.Option(
        ..., '--control-id', '-cid', help="Control Identifier. Try: `ls controls all` command"
    ),
):
    if not control_id in ALL_GUARDRAILS:
        raise typer.Exit(
            f"Given Control ID: {control_id} is not found in the list. Try: `ls controls all` command"
        )


@app.command("sync")
def _sync_organizational_unit_controls(
    from_organizational_unit: str = typer.Option(
        ..., '--from-organizational-unit','-fou', help="ID or Name of Organizational Unit to get the controls from."
    ),
    to_organizational_unit: str = typer.Option(
        ..., '--to-organizational-unit' ,'-tou', help="ID or Name of Organizational Unit to apply GuardRail controls to."
    ),
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
    _print_list_of_guardrails(STRONGLY_RECOMMENDED_GUARDRAILS, "STRONGLY RECOMMENDED GUARDRAILS")


def print_boto_region_and_profile():
    profile = session.profile_name
    region = session.region_name
    result = f"--region: [bold]{region}[/]"
    if profile:
        result = f"--profile: [bold]{profile}[/] | " + result
    result = f"awscli: " + result
    
    console.print(result, style='blue on white', justify='center')
    
if __name__ == "__main__":
    # typer.run(main)
    # list_roots()
    # get_organizational_units()
    # list_accounts()
    # main()
    # check_control_tower_available_on_region()
    
    
    sanity_checks()
    console.print("kloia/ctower v.0.1", style='green on white', justify='center')
    print_boto_region_and_profile()
    console.print()
    
    app()


"""
ctower ls organizational-units
ctower ls controls [all,elective,data-residency,strongly-recommended]
ctower ls enabled-controls --ou <ou-id>
ctower sync --from ou-id --to ou-id 
ctower apply ou-id GUARDRAILID 


"""
