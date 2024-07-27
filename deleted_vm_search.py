"""
GCP Deleted VM Search, v1 AUTHOR: michael.quintero@rackspace.com
PURPOSE: To search specifically for deleted vms within a given date/time range for either a known project or to search through all projects which account is allowed access to
Additional Info: https://cloud.google.com/sdk/gcloud/reference/logging/read
Usage: deleted_vm_search.py, answer the questions, bam!
Note: User is expected to have already set credentials and run 'gcloud auth application-default login'. Doing so is used to auth your local dev env with Google Cloud using your user credentials. 
Useful when you're developing applications or scripts that interact with Google Cloud services.
"""

import subprocess
from google.cloud import logging, compute_v1
from datetime import datetime, timedelta

def get_user_input():
    # Get start timestamp
    while True:
        timestamp_start = input("Enter the start timestamp (YYYY-MM-DDTHH:MM:SSZ): ")
        try:
            datetime.strptime(timestamp_start, "%Y-%m-%dT%H:%M:%SZ")
            break
        except ValueError:
            print("Invalid format. Please enter the timestamp in the format YYYY-MM-DDTHH:MM:SSZ")

    # Get end timestamp
    while True:
        timestamp_end = input("Enter the end timestamp (YYYY-MM-DDTHH:MM:SSZ): ")
        try:
            datetime.strptime(timestamp_end, "%Y-%m-%dT%H:%M:%SZ")
            break
        except ValueError:
            print("Invalid format. Please enter the timestamp in the format YYYY-MM-DDTHH:MM:SSZ")

    instance_id = input("Enter the instance ID: ")
    project_id = input("Enter the project ID (leave blank to search all projects): ")
    return timestamp_start, timestamp_end, instance_id, project_id

def list_projects():
    try:
        result = subprocess.run(['gcloud', 'projects', 'list', '--format=value(projectId)'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        projects = result.stdout.strip().split('\n')
        return projects
    except subprocess.CalledProcessError as e:
        print(f"Error listing projects: {e.stderr}")
        return []

def check_compute_api_enabled(project_id):
    try:
        compute_client = compute_v1.InstancesClient()
        compute_client.list(project=project_id, zone='us-central1-a')
        return True
    except Exception:
        return False

def query_logs(timestamp_start, timestamp_end, instance_id, project_id=None):
    if project_id:
        projects = [project_id]
    else:
        print("Fetching projects...")
        projects = [project for project in list_projects() if check_compute_api_enabled(project)]

    for project in projects:
        client = logging.Client(project=project)

        # Construct the filter string
        filter_str = (
            f'severity="NOTICE" AND '
            f'resource.type="gce_instance" AND '
            f'timestamp>="{timestamp_start}" AND '
            f'timestamp<="{timestamp_end}" AND '
            f'resource.labels.instance_id="{instance_id}" AND '
            f'protoPayload.methodName="v1.compute.instances.delete"'
        )

        # Query logs
        print(f"Running query for project {project}...")
        entries = client.list_entries(filter_=filter_str)

        for entry in entries:
            print(format_log_entry(entry))
            return  # Stop processing once a record is found

def format_log_entry(entry):
    log_info = {
        "log_name": entry.log_name,
        "insert_id": entry.insert_id,
        "severity": entry.severity,
        "timestamp": entry.timestamp,
        "instance_id": entry.resource.labels.get('instance_id', 'N/A'),
        "zone": entry.resource.labels.get('zone', 'N/A'),
        "project_id": entry.resource.labels.get('project_id', 'N/A'),
        "method_name": entry.payload.get('methodName', 'N/A'),
        "resource_name": entry.payload.get('resourceName', 'N/A'),
        "principal_email": entry.payload.get('authenticationInfo', {}).get('principalEmail', 'N/A'),
        "caller_ip": entry.payload.get('requestMetadata', {}).get('callerIp', 'N/A'),
        "user_agent": entry.payload.get('requestMetadata', {}).get('callerSuppliedUserAgent', 'N/A'),
    }
    formatted_entry = (
        f"Log Name: {log_info['log_name']}\n"
        f"Insert ID: {log_info['insert_id']}\n"
        f"Severity: {log_info['severity']}\n"
        f"Timestamp: {log_info['timestamp']}\n"
        f"Instance ID: {log_info['instance_id']}\n"
        f"Zone: {log_info['zone']}\n"
        f"Project ID: {log_info['project_id']}\n"
        f"Method Name: {log_info['method_name']}\n"
        f"Resource Name: {log_info['resource_name']}\n"
        f"Principal Email: {log_info['principal_email']}\n"
        f"Caller IP: {log_info['caller_ip']}\n"
        f"User Agent: {log_info['user_agent']}\n"
        "----------------------------------------"
    )
    return formatted_entry

def main():
    timestamp_start, timestamp_end, instance_id, project_id = get_user_input()
    query_logs(timestamp_start, timestamp_end, instance_id, project_id)

if __name__ == "__main__":
    main()
