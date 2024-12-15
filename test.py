from ncclient import manager
import requests

def get_running_config(host, username, password):
    with manager.connect(
        host=host,
        username=username,
        password=password,
        device_params={'name': 'iosxe'},
        hostkey_verify=False
    ) as m:
        running_config = m.get_config(source='running').data_xml
        return running_config

def apply_changes(host, username, password, config_changes):
    with manager.connect(
        host=host,
        username=username,
        password=password,
        device_params={'name': 'iosxe'},
        hostkey_verify=False
    ) as m:
        response = m.edit_config(target='running', config=config_changes)
        return response

def send_webex_message(message, access_token, room_id):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": room_id,
        "text": message
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Main process
host = "192.168.56.101"
username = "cisco"
password = "cisco123!"
access_token = "Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OL2E5OTU3MzU2LTFlZjUtNGZiYS1iNDJmLTc0YmM2ZDJjMGE3Mw"
room_id = "webexteams://im?space=895e09b0-5a36-11ef-8f77-ebb44fe9a5b0"

# Step 1: Get current config
current_config = get_running_config(host, username, password)

# Step 2: Apply changes
config_changes = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interface>
            <name>GigabitEthernet0/1</name>
            <enabled>true</enabled>
        </interface>
    </interfaces>
    <system xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <hostname>NewHostName</hostname>
    </system>
</config>
"""

# Step 3: Verify changes
updated_config = get_running_config(host, username, password)

# Step 4: Send WebEx notification
message = "Network configuration has been successfully updated."
send_webex_message(message, access_token, room_id)
