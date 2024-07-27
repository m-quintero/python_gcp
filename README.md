# GCP Deleted VM Search

## Overview
To help searche specifically for deleted VMs within a given date/time range for either a known project or to search through all projects which the account has access to. It'll help identify & fetch logs of deleted VMs in Google Cloud Platform (GCP).

## Additional Info
For more details, refer to the [gcloud logging read documentation](https://cloud.google.com/sdk/gcloud/reference/logging/read).

## Prerequisites
- Python 3.6 or higher
- Google Cloud SDK installed and configured
- Authentication set up using `gcloud auth application-default login`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/m-quintero/python_gcp.git
    cd python_gcp
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

### Authentication
Run the following command to authenticate your local development environment with Google Cloud:

```sh
gcloud auth application-default login
```
## Usage
1. Ensure you have the required Python packages installed.
2. Set up your Google Cloud credentials.
3. Run the script and answer the prompts.

### Running the Script
Execute the script by running:

```sh
python3 deleted_vm_search.py
```

### Prompts
You will be prompted to enter the following details:
- Start timestamp (format: `YYYY-MM-DDTHH:MM:SSZ`)
- End timestamp (format: `YYYY-MM-DDTHH:MM:SSZ`)
- Instance ID
- Project ID (leave blank to search all projects)

### Example
```sh
Enter the start timestamp (YYYY-MM-DDTHH:MM:SSZ): 2024-07-25T00:00:00Z
Enter the end timestamp (YYYY-MM-DDTHH:MM:SSZ): 2024-07-27T23:59:00Z
Enter the instance ID: 5395914502502749792
Enter the project ID (leave blank to search all projects):
```

## Note
User is expected to have already set credentials and run `gcloud auth application-default login`. This command is used to authenticate your local development environment with Google Cloud using your user credentials. It's useful when you're developing applications or scripts that interact with Google Cloud services.

## Requirements
The script requires the following Python packages:

- google-cloud-logging
- google-cloud-compute

These packages are listed in the `requirements.txt` file.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Michael Quintero (michael.quintero@rackspace.com or michael.quintero@gmail.com)
