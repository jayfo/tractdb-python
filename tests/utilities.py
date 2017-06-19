import base.docker.docker_commands
import nose.tools
import tractdb.client
import yaml


class Utilities:
    def __init__(self, cls_context):
        self._context = cls_context.__name__

    @classmethod
    def client_admin(cls):
        # Read the admin credentials
        with open('tests/test-secrets/secrets_couchdb.yml') as f:
            couchdb_secrets = yaml.safe_load(f)

        admin_account = couchdb_secrets['admin']['user']
        admin_password = couchdb_secrets['admin']['password']

        # Create the client
        client_admin = tractdb.client.TractDBClient(
            tractdb_url=cls.url_base_pyramid(),
            account=admin_account,
            password=admin_password
        )

        return client_admin

    @classmethod
    def client(cls, *, account, password):
        # Create the client
        client = tractdb.client.TractDBClient(
            tractdb_url=cls.url_base_pyramid(),
            account=account,
            password=password
        )

        return client

    def delete_account(self, *, account, client_admin=None):
        if client_admin is None:
            client_admin = self.client_admin()

        if client_admin.exists_account(account=account):
            client_admin.delete_account(account=account)

    def delete_all_documents(self, *, client):
        docs = client.get_documents()
        for doc in docs:
            client.delete_document(doc=doc)

    def ensure_fresh_account(self, *, account, password, client_admin=None):
        if client_admin is None:
            client_admin = self.client_admin()

        # Ensure the account does not already exist
        if client_admin.exists_account(account=account):
            client_admin.delete_account(account=account)

        # Create the account we expect
        client_admin.create_account(account=account, password=password)

    def test_account_name(self, *, account_index=0):
        return 'account_{}_{}'.format(
            self._context,
            account_index
        ).lower()

    def test_account_password(self, *, account_index=0):
        return 'password_{}_{}'.format(
            self._context,
            account_index
        ).lower()

    def test_document(self, *, document_index=0):
        return {
            'test_field':
                'content_{}_{}'.format(
                    self._context,
                    document_index
                ),
            'another_test_field':
                'content_{}_{}'.format(
                    self._context,
                    document_index
                )
        }

    def test_document_id(self, *, document_index=0):
        return 'document_id_{}_{}'.format(
            self._context,
            document_index
        ).lower()

    def test_role(self, *, role_index=0):
        return 'role_{}_{}'.format(
            self._context,
            role_index
        ).lower()

    @staticmethod
    def url_base_pyramid():
        return 'http://{}:{}'.format(
            base.docker.docker_commands.machine_ip(),
            '8080'
        )
