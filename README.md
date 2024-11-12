# AzureCredentialRotation
Azure Credential Rotation is a Python-based solution that automates the process of rotating credentials, such as service principal secrets or managed identities, in Azure. It ensures secure access management by regularly updating credentials, reducing the risk of unauthorized access while minimizing manual intervention.


## Steps

1. Create a subscription with Microsoft Azure Cloud Platform
2. Download and install Azure CLI.
3. Create an Azure Key Vault. I created my key vault through the microsoft azure platform but it could easily be created on the Azure CLI. 
4. Install Python (I am using 3.10).
5. Use 'az login --use-device-code' to login to Azure web services.
6. Run python script to automate key rotation within the key vault.


## Future Additions
For future additions, we could add logging for recovery or critical events during the rotation process.
