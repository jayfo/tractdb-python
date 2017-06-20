import base64
import requests
import tractdb.client
import yaml


def main():
    with open('secrets/tractdb.fitbit.yml', 'r') as f:
        config = yaml.safe_load(f)

    for account in config['secrets']['accounts'].keys():
        # Start a client
        client = tractdb.client.TractDBClient(
            tractdb_url=config['tractdb_url'],
            account=config['secrets']['accounts'][account]['account'],
            password=config['secrets']['accounts'][account]['password']
        )

        # Start a session with Fitbit
        session_fitbit = requests.Session()

        # If a code is available
        if client.exists_document(doc_id='fitbit_callback_code'):
            print('Found callback code.')

            # Get the code
            doc_code = client.get_document(doc_id='fitbit_callback_code')

            # Convert it to a token
            response = session_fitbit.post(
                'https://api.fitbit.com/oauth2/token',
                headers={
                    'Authorization':
                        'Basic {}'.format(
                            base64.b64encode('{}:{}'.format(
                                config['secrets']['fitbit']['id'],
                                config['secrets']['fitbit']['secret']
                            ).encode('utf-8')).decode('utf-8')
                        )
                },
                data={
                    'grant_type': 'authorization_code',
                    'client_id': config['secrets']['fitbit']['id'],
                    'code': doc_code['callback_code'],
                    'redirect_uri': config['secrets']['fitbit']['redirect']
                }
            )

            if response.status_code == 200:
                print('Obtained token.')

                doc_token = response.json()

                # Remove the code
                client.delete_document(doc=doc_code)

                # Remove any old token
                doc_token_existing = client.exists_document(doc_id='fitbit_token')
                if doc_token_existing:
                    client.delete_document(doc=doc_token_existing)

                # Store the token
                client.create_document(doc=doc_token, doc_id='fitbit_token')
            elif response.status_code == 400:
                if 'Authorization code invalid' in response.json()['errors'][0]['message']:
                    print('Callback code invalid.')

                    # Remove the code
                    client.delete_document(doc=doc_code)

if __name__ == '__main__':
    main()
