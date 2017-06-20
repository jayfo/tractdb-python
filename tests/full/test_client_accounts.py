import nose.tools
import tests.utilities


class TestClientAccounts:
    @classmethod
    def setup_class(cls):
        cls.utilities = tests.utilities.Utilities(cls)

    def test_create_and_delete_account(self):
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

        # The account does not exist
        nose.tools.assert_false(
            client_admin.exists_account(
                account=cls.utilities.test_account_name()
            )
        )

        nose.tools.assert_not_in(
            cls.utilities.test_account_name(),
            client_admin.get_accounts()
        )

        # Create it
        client_admin.create_account(
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

        # Creating it again fails
        nose.tools.assert_raises(
            Exception,
            client_admin.create_account,
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

        # The account exists
        nose.tools.assert_true(
            client_admin.exists_account(
                account=cls.utilities.test_account_name()
            )
        )

        nose.tools.assert_in(
            cls.utilities.test_account_name(),
            client_admin.get_accounts()
        )

        # Delete it
        client_admin.delete_account(
            account=cls.utilities.test_account_name()
        )

        # Deleting it again fails
        nose.tools.assert_raises(
            Exception,
            client_admin.delete_account,
            account=cls.utilities.test_account_name()
        )

        # The account does not exist
        nose.tools.assert_false(
            client_admin.exists_account(
                account=cls.utilities.test_account_name()
            )
        )

        nose.tools.assert_not_in(
            cls.utilities.test_account_name(),
            client_admin.get_accounts()
        )
