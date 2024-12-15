from unittest.mock import Mock, patch

# Simulating the get_running_config function
def simulate_get_running_config():
    # Mocked XML response (simulating device configuration)
    simulated_config = """
    <config>
        <interfaces>
            <interface>
                <name>GigabitEthernet0/1</name>
                <status>up</status>
            </interface>
        </interfaces>
        <hostname>SimulatedHost</hostname>
    </config>
    """
    return simulated_config

# Testing the simulation
def test_get_running_config_simulation():
    with patch('__main__.get_running_config', new=Mock(return_value=simulate_get_running_config())):
        # Replace 'host', 'username', 'password' with test placeholders
        host = "test_host"
        username = "test_user"
        password = "test_pass"
        
        # Call the simulated function
        result = get_running_config(host, username, password)
        
        # Print results for demonstration
        print("Simulated Config Output:")
        print(result)

# Run the test simulation
test_get_running_config_simulation()
