from ncclient import manager
import requests
import datetime

# Function to get running configuration
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

# Function to backup configuration to a file
def backup_config(config, filename="backup_config.xml"):
    with open(filename, "w") as file:
        file.write(config)

# Function to apply configuration changes
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

# Function to send WebEx notifications
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
access_token = "Y2lzY29zcGFyazovL3VzL0FQUExJQ2FUSU9OL2E5OTU3MzU2LTFlZjUtNGZiYS1iNDJmLTc0YmM2ZDJjMGE3Mw"
room_id = "webexteams://im?space=895e09b0-5a36-11ef-8f77-ebb44fe9a5b0"

# Step 1: Backup current configuration
current_config = get_running_config(host, username, password)
backup_config(current_config, "backup_config.xml")

# Step 2: Apply configuration changes
config_changes = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interface>
            <enabled>true</enabled>
        </interface>
    </interfaces>
    <system xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <hostname>NewHostName</hostname>
    </system>
</config>
"""
apply_response = apply_changes(host, username, password, config_changes)

# Step 3: Validate changes
updated_config = get_running_config(host, username, password)
validation_success = config_changes.strip() in updated_config

# Step 4: Notify via WebEx
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if validation_success:
    message = f"[{timestamp}] Network configuration updated successfully."
else:
    message = f"[{timestamp}] Configuration update failed. Review changes."
send_webex_message(message, access_token, room_id)
