import nose.tools
import tests.utilities
import tractdb.client
import yaml


class TestClient:
    @classmethod
    def setup_class(cls):
        cls.utilities = tests.utilities.Utilities(cls)

    def test_create_client(self):
        cls = type(self)

        # Get an admin
        client_admin = cls.utilities.client_admin()

        # If the account exists, it's left from a prior test
        try:
            client_admin.delete_account(
                account=cls.utilities.test_account_name()
            )
        except Exception:
            pass

        # Create the account
        client_admin.create_account(
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

        # Create a session to the new account
        client = tractdb.client.TractDBClient(
            tractdb_url=cls.utilities.url_base_pyramid(),
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

        # Peek inside to ensure we got a session
        nose.tools.assert_is_not_none(
            client._session
        )

        # Remove the account
        client_admin.delete_account(
            account=cls.utilities.test_account_name()
        )

    def test_create_client_admin(self):
        cls = type(self)

        # Read the admin credentials
        with open('tests/test-secrets/secrets_couchdb.yml') as f:
            couchdb_secrets = yaml.safe_load(f)

        admin_account = couchdb_secrets['admin']['user']
        admin_password = couchdb_secrets['admin']['password']

        # Create the session
        client_admin = tractdb.client.TractDBClient(
            tractdb_url=cls.utilities.url_base_pyramid(),
            account=admin_account,
            password=admin_password
        )

        # Peek inside to ensure we got a session
        nose.tools.assert_is_not_none(
            client_admin._session
        )
