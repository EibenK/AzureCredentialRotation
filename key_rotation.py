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
KEY_VAULT_NAME = ""
KEY_NAME = ""


# Function to run Azure CLI commands and capture detailed output
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
        logging.error(f"stderr: {e.stderr}")
        logging.error(f"stdout: {e.stdout}")
        return None


# Function to check if a key exists in the Key Vault
def check_key_exists():
    command = [
        "az", "keyvault", "key", "list",
        "--vault-name", KEY_VAULT_NAME,
        "--query", f"[?name=='{KEY_NAME}'].name",  # Filter by key name
        "--output", "json"
    ]
    
    logging.info(f"Checking if key '{KEY_NAME}' exists in Key Vault: {KEY_VAULT_NAME}")
    result = run_azure_cli_command(command)

    if result is None:
        logging.error("Failed to retrieve key list from Key Vault.")
        return False

    keys = json.loads(result)

    if keys:
        logging.info(f"Key '{KEY_NAME}' exists in the Key Vault.")
        return True
    else:
        logging.info(f"Key '{KEY_NAME}' does not exist in the Key Vault.")
        return False


# Function to check if a key is in a deleted but recoverable state
def check_key_deleted():
    command = [
        "az", "keyvault", "key", "show",
        "--vault-name", KEY_VAULT_NAME,
        "--name", KEY_NAME,
        "--output", "json"
    ]
    
    logging.info(f"Checking if key '{KEY_NAME}' is in a deleted but recoverable state.")
    result = run_azure_cli_command(command)

    if result is None:
        logging.error("Failed to retrieve key details from Key Vault.")
        return False

    key_details = json.loads(result)
    if 'deletedDate' in key_details:  # Key is in a deleted state
        logging.info(f"Key '{KEY_NAME}' is in a deleted but recoverable state.")
        return True

    return False


# Function to purge a deleted key (permanently delete it)
def purge_deleted_key():
    command = [
        "az", "keyvault", "key", "purge",
        "--vault-name", KEY_VAULT_NAME,
        "--name", KEY_NAME
    ]
    logging.info(f"Purging the deleted key '{KEY_NAME}' from Key Vault.")
    run_azure_cli_command(command)


# Function to disable the current key
def disable_key():
    command = [
        "az", "keyvault", "key", "set-attributes",
        "--vault-name", KEY_VAULT_NAME,
        "--name", KEY_NAME,
        "--enabled", "false"  # Disable the key
    ]
    logging.info(f"Disabling the current key '{KEY_NAME}' in Key Vault.")
    run_azure_cli_command(command)


# Function to create a new key
def create_key():
    command = [
        "az", "keyvault", "key", "create",
        "--vault-name", KEY_VAULT_NAME,
        "--name", KEY_NAME,
        "--kty", "RSA",  # Key type (RSA for example)
        "--size", "2048"  # Key size
    ]
    logging.info(f"Creating new key '{KEY_NAME}' in Key Vault.")
    result = run_azure_cli_command(command)
    if result:
        logging.info(f"Successfully created new key '{KEY_NAME}' in the Key Vault.")
    else:
        logging.error(f"Failed to create new key '{KEY_NAME}'.")


# Main function to check, purge, disable and create key
def manage_key():
    # Step 1: Check if the key is in a deleted but recoverable state
    if check_key_deleted():
        # Step 2: If the key is in deleted state, purge it
        purge_deleted_key()

    # Step 3: Check if the key exists before disabling it
    if check_key_exists():
        # Step 4: Disable the current key before creating a new one
        disable_key()

    # Step 5: Create a new key
    create_key()


# Main execution
if __name__ == "__main__":
    manage_key()
