import base64
import requests
import tractdb.client
import yaml


def refresh_token(*, config, client, session_fitbit):
    # If a token is available
    doc_token_existing = client.exists_document(doc_id='fitbit_token')
    if doc_token_existing:
        print('Found existing token.')

        # Get the token
        doc_token_existing = client.get_document(doc_id='fitbit_token')

        # Renew the token
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
                'grant_type': 'refresh_token',
                'refresh_token': doc_token_existing['refresh_token'],
                'redirect_uri': config['secrets']['fitbit']['redirect']
            }
        )

        if response.status_code == 200:
            print('Refreshed token.')

            doc_token = response.json()

            # Replace the token
            client.update_document(
                doc=doc_token,
                doc_id=doc_token_existing['_id'],
                doc_rev=doc_token_existing['_rev']
            )

            return doc_token
    else:
        print('No token found.')

        return None


def download(*, config, client, session_fitbit, token):
    # response = session_fitbit.get(
    #     'https://api.fitbit.com/1/user/{}/devices.json'.format(
    #         token['user_id']
    #     ),
    #     headers={
    #         'Authorization':
    #             'Bearer {}'.format(token['access_token'])
    #     }
    # )
    #
    # response = session_fitbit.get(
    #     'https://api.fitbit.com/1/user/{}/activities/date/{}.json'.format(
    #         token['user_id'],
    #         '2017-06-20'
    #     ),
    #     headers={
    #         'Authorization':
    #             'Bearer {}'.format(token['access_token'])
    #     }
    # )

    for current_year in ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']:
        response = session_fitbit.get(
            'https://api.fitbit.com/1/user/{}/activities/steps/date/{}/1y.json'.format(
                token['user_id'],
                '{}-12-31'.format(current_year)
            ),
            headers={
                'Authorization':
                    'Bearer {}'.format(token['access_token'])
            }
        )

        try:
            print('{}: {} days with steps'.format(
                current_year,
                len(
                    [day for day in response.json()['activities-steps'] if int(day['value']) > 0]
                )
            ))
        except KeyError:
            print(response.json())


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

        token = refresh_token(config=config, client=client, session_fitbit=session_fitbit)
        if token:
            download(config=config, client=client, session_fitbit=session_fitbit, token=token)


if __name__ == '__main__':
    main()
