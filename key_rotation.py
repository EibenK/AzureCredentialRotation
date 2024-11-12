import subprocess
import logging
import json

# Set up logging to capture output in a file
logging.basicConfig(
    filename='keyvault_keys_check.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Azure Key Vault details
KEY_VAULT_NAME = "<<Key Vault Name Goes Here>>"


# Function to run Azure CLI commands
def run_azure_cli_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=True
            )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")
        return None


# Function to check if there are keys in the Key Vault
def check_keys_in_keyvault():
    command = [
        "az", "keyvault", "key", "list",
        "--vault-name", KEY_VAULT_NAME,
        "--query", "[].name",  # Return only the names of the keys
        "--output", "json"
    ]
    
    logging.info(f"Checking for keys in Key Vault: {KEY_VAULT_NAME}")
    result = run_azure_cli_command(command)

    if result is None:
        logging.error("Failed to retrieve key list from Key Vault.")
        return

    # Parse the result as JSON to get the list of keys
    keys = json.loads(result)

    if keys:
        logging.info(f"Found {len(keys)} key(s) in the Key Vault: {keys}")
    else:
        logging.info(f"No keys found in the Key Vault: {KEY_VAULT_NAME}")


# Main function
if __name__ == "__main__":
    check_keys_in_keyvault()
