import unittest
import requests
import os
import base64
from main import get_github_user, create_or_update_contact

class TestGitHubFreshdeskIntegration(unittest.TestCase):
    def test_get_github_user_success(self):
        # Llamada a la función a probar
        result = get_github_user('Engleonardorm7')

        # Comprobación de los resultados
        self.assertEqual(result['name'], 'Leonardo Rodriguez')
        self.assertEqual(result['email'], 'leonardorm7@hotmail.com')
        self.assertEqual(result['company_id'], None)
        self.assertEqual(result['twitter_id'], None)

    def test_create_or_update_contact_existing_contact(self):
        # Datos de contacto
        contact_data = {
            'name': 'Leonardo Rodriguez',
            'email': 'example@hotmail.com',
            'company_id': None,
            'twitter_id': None
        }

        # Llamada a la función a probar
        create_or_update_contact('leonardorm7', contact_data)
        api_key = os.getenv('FRESHDESK_TOKEN')
        encoded_api_key = base64.b64encode(api_key.encode()).decode()
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_api_key}'
        }
        # Comprobación de que se creó o actualizó el contacto correctamente
        response = requests.get('https://leonardorm7.freshdesk.com/api/v2/contacts',headers=headers)
        self.assertEqual(response.status_code, 200)
        contacts = response.json()
        existing_contact = next((contact for contact in contacts if contact['email'] == contact_data['email']), None)
        self.assertIsNotNone(existing_contact)

    # Agrega más pruebas unitarias según sea necesario

if __name__ == '__main__':
    unittest.main()
