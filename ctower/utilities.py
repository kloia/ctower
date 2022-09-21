from tabulate import tabulate
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.traceback import install
from functools import lru_cache
from rich.prompt import Confirm
import boto3
from typing import Optional
import typer
import json
from termcolor import colored
from . import guardrail_identifiers


def _create_boto_session():
    profile_name = os.environ.get("AWS_PROFILE", False)
    region_name = os.environ.get("AWS_REGION", False)
    _kwargs_dict = {}
    if profile_name:
        _kwargs_dict["profile_name"] = profile_name
    if region_name:
        _kwargs_dict["region_name"] = region_name
    session = boto3.session.Session(**_kwargs_dict)
    return session


session = _create_boto_session()
console = Console(record=True)
ct_client = session.client("controltower")


def get_boto_session():
    return session


def get_rich_console():
    return console


def get_control_tower_client():
    return ct_client


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


@lru_cache(maxsize=None)
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

def get_control_id_from_control_identifier(control_identifier):
    prev_arn, control_id = control_identifier.rsplit("/", 1)
    return control_id

def _list_enabled_controls(organizational_unit_arn):
    try:
        response = call_boto3_function(
            ct_client,
            "list_enabled_controls",
            kwargs={"targetIdentifier": organizational_unit_arn},
        )
        enabled_controls = response.get("enabledControls", [])
        enabled_control_identifiers = [ec.get("controlIdentifier") for ec in enabled_controls]
        return enabled_control_identifiers
    except ct_client.exceptions.ResourceNotFoundException as e:
        console.print(
            Panel(
                f"[red][bold]Failed to list enabled guardrail controls[/][/] on Organizational Unit: [blue]{organizational_unit_arn}[/].\n[yellow]This Organizational Unit [bold]is not registered[/] with AWS Control Tower.\n[white]Maybe you set the wrong [bold]AWS_REGION[/] environment variable?",
                title="[red][bold]ERROR",
                title_align="center",
                expand=True,
            )
        )
        raise typer.Exit()


def find_organizational_unit_by_id_or_name(id_or_name: str):
    organizational_units = get_organizational_units()
    for o_u in organizational_units:
        if o_u.get("Id") == id_or_name or o_u.get("Name") == id_or_name:
            return o_u
    return False


def find_guardrail_control_by_id(control_id):
    for gr_control in guardrail_identifiers.ALL_GUARDRAILS:
        if gr_control.get("id") == control_id:
            return gr_control
    return False






def _get_control_operation(operation_identifier):
    try:
        response = ct_client.get_control_operation(
            operationIdentifier=operation_identifier
        )
    except Exception as e:
        print_error_panel(
            f"[bold]Failed to query Control Operation with ID: [blue]{operation_identifier}[/]"
        )
        raise typer.Exit()
    return response.get("controlOperation", False)


def print_error_panel(text):
    panel = Panel(
        text,
        title="[red][bold]ERROR",
        title_align="left",
        expand=True,
    )
    console.print(panel)
    return panel


def print_success_panel(text):
    panel = Panel(
        text,
        title="[green][bold]SUCCESS",
        title_align="left",
        expand=True,
    )
    console.print(panel)
    return panel
