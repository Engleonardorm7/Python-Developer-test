import requests
import os
import base64

def get_github_user(username):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {github_token}'}
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        username = user_data['login']
        email = user_data['email']
        name = user_data['name']
        company = user_data['company']
        twitter_username=user_data['twitter_username']
        contact_data = {
        "name": name,
        "email": email,
        "company_id": company,
        "twitter_id": twitter_username
        }
        return contact_data
    else:
        raise Exception(f'Error retrieving GitHub user: {response.text}')


def create_or_update_contact(subdomain, contact_data):
    api_key = os.getenv('FRESHDESK_TOKEN')
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    endpoint = f'https://{subdomain}.freshdesk.com/api/v2/contacts'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_api_key}'
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        contacts = response.json()
        existing_contact = next((contact for contact in contacts if contact['email'] == contact_data['email']), None)
        if existing_contact:
            print("Contact already exist")
            contact_id = existing_contact['id']
            update_endpoint = f'{endpoint}/{contact_id}'
            # print(update_endpoint)
            response = requests.put(update_endpoint, json=contact_data, headers=headers)
            if response.status_code == 200:
                print("Contact updated successfully.")
            else:
                print(f"Failed to update contact. Status code: {response.status_code}")
        else:
            response = requests.post(endpoint, json=contact_data, headers=headers)
            if response.status_code == 201:
                print("Contact created successfully.")
            else:
                print(f"Failed to create contact. Status code: {response.status_code}")
    else:
        print(f"Failed to retrieve contacts. Status code: {response.status_code}")


if __name__ == '__main__':

    username=input("Type your username: \n")

    github_user = get_github_user(username)
    # print(github_user)
    freshdesk_subdomain=input("Type the domain: \n")
    # contact_data = {
    #     "name": "carlos Schock",
    #     "email": "prueba@example.com",
    #     "twitter_id": "twitter_username"
    # }

    create_or_update_contact(freshdesk_subdomain, github_user)