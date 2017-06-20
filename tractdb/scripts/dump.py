import tractdb.client
import yaml

if __name__ == '__main__':
    with open('secrets/tractdb.dump.yml', 'r') as f:
        config = yaml.safe_load(f)

    for account in config['secrets']['accounts'].keys():
        client = tractdb.client.TractDBClient(
            tractdb_url=config['tractdb_url'],
            account=config['secrets']['accounts'][account]['account'],
            password=config['secrets']['accounts'][account]['password']
        )

        print(client.get_documents())
