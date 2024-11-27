import time
import requests
import json

def get_task_1(access_token, process_instance_key):
    url = "https://bru-2.tasklist.camunda.io:443/eea87386-0393-4bbc-ad2e-a10a85bb2646/v1/tasks/search"  
    headers = {
            'Authorization' : f'Bearer {access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    data = json.dumps({
        'processInstanceKey': f'{process_instance_key.process_instance_key}',
        'processName': 'Wiedzmin',
        'taskDefinitionId': 'Activity_1'
    })

    print()
    loading = True

    while loading:
        response = requests.post(url, headers=headers, data=data)
        if (response.status_code == 200):
                if (response.json() != []):  
                    loading = False

                    task_id = response.json()[0]['id']
                    print("\nTask list request response: ", response.status_code)
                    print("Task 1 ID: ", task_id)
                else:
                    print("Loading...")
                    time.sleep(2)
    
    return task_id



def complete_task_1(access_token, task_id, is_miasto):
    url = f"https://bru-2.tasklist.camunda.io:443/eea87386-0393-4bbc-ad2e-a10a85bb2646/v1/tasks/{task_id}/complete"
    data = json.dumps({
    'variables': [
        {
        'name': 'is_miasto',
        'value': is_miasto
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization' : f'Bearer {access_token}'
    }

    response = requests.patch(url, headers=headers, data=data)
    print("Task 1 completion request response: ", response.status_code)


def get_task_2(access_token, process_instance_key):
    url = "https://bru-2.tasklist.camunda.io:443/eea87386-0393-4bbc-ad2e-a10a85bb2646/v1/tasks/search"  
    headers = {
            'Authorization' : f'Bearer {access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    data = json.dumps({
        'processInstanceKey': f'{process_instance_key.process_instance_key}',
        'processName': 'Wiedzmin',
        'taskDefinitionId': 'Activity_3'
    })

    print()
    loading = True

    while loading:
        response = requests.post(url, headers=headers, data=data)
        if (response.status_code == 200):
                if (response.json() != []):
                    loading = False

                    task_id = response.json()[0]['id']
                    print("\nTask list request response: ", response.status_code)
                    print("Task 2 ID: ", task_id)
                else:
                    print("Loading...")
                    time.sleep(2)

    return task_id



def complete_task_2(access_token, task_id, monster_identified):
    url = f"https://bru-2.tasklist.camunda.io:443/eea87386-0393-4bbc-ad2e-a10a85bb2646/v1/tasks/{task_id}/complete"
    data = json.dumps({
    'variables': [
        {
        'name': 'monster_identified',
        'value': monster_identified
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization' : f'Bearer {access_token}'
    }

    response = requests.patch(url, headers=headers, data=data)
    print("Task 2 completion request response: ", response.status_code)