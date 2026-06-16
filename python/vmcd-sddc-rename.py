#!/usr/bin/env python3

import argparse
import requests                         # need this for Get/Post/Delete
import json
import sys


ap = argparse.ArgumentParser(
                prog = 'VMware Cloud on Dell SDDC rename utility',
                description = 'A Command-line utility to be used to rename a VMware Cloud on Dell SDDC.',
                )

# ============================
# define arguments
# ============================
ap.add_argument('-oid', '--org_id', required=True, help="The ID of the VMware Cloud Organization.")
ap.add_argument('-t', '--refresh_token', required=True, help="The user's refresh token for the VMware Cloud org.  User must be an Org Member, and be assigned the VMC on Dell Administrator role.")
ap.add_argument('-sid', '--sddc_id', required=True, help="The ID of the VMware Cloud on Dell SDDC to be renamed.")
ap.add_argument('-n', '--new_sddc_name', required=True, help="The new name of the VMware Cloud on Dell SDDC.")
ap.add_argument('-v', '--validate_only', action="store_true", help="The new name of the VMware Cloud on Dell SDDC.")

# ============================
# Parse arguments
# ============================
args = ap.parse_args()

# ============================
# instantiate variables
# ============================
my_token = args.refresh_token
orgid = args.org_id
sddcid = args.sddc_id
newname = args.new_sddc_name
val = args.validate_only

# ============================
# print output for review instead of executing
# ============================
if val is True:
    print()
    print("Validating input only:")
    print()
    print(f'You have specified your refresh token as {my_token}')
    print()
    print(f'You have specified your ORG ID as {orgid}')
    print()
    print(f'You have specified the SDDC to be renamed as {sddcid}')
    print()
    print(f'You have specified the new name of the SDDC as {newname}')
    print()
    print("exiting")
    sys.exit()
else:
    pass

# get an access token
token_params = {'refresh_token': my_token}
token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
token_response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize',params=token_params, headers=token_headers)
token_json = token_response.json()
access_token = token_json['access_token']

# rename the SDDC
rename_header = {'csp-auth-token': access_token}
rename_url = f'https://vmc.vmware.com/vmc/fractal/api/orgs/{orgid}/edges/{sddcid}'
rename_data = {"location_name" : newname}
rename_response = requests.patch(rename_url, headers=rename_header, json=rename_data)
json_response = rename_response.json()
if rename_response.status_code == 200:
    print(f'The SDDC has been renamed to {newname}')
else:
    print("There was an error. Check the syntax.")
    print(f'API call failed with status code {rename_response.status_code}. URL: {rename_url}.')
    sys.exit(json_response['error_message'])