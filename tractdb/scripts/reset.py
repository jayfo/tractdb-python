import tractdb.client
import yaml

if __name__ == '__main__':
    with open('secrets/tractdb.reset.yml', 'r') as f:
        config = yaml.safe_load(f)

    client = tractdb.client.TractDBClient(
        tractdb_url=config['tractdb_url'],
        account=config['secrets']['admin']['user'],
        password=config['secrets']['admin']['password']
    )

    if client.exists_account(account='jayfo'):
        client.delete_account(account='jayfo')

    client.create_account(account='jayfo', password='jayfo')
