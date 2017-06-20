import nose.tools
import tests.utilities


class TestClientRoles:
    @classmethod
    def setup_class(cls):
        cls.utilities = tests.utilities.Utilities(cls)

        # Ensure we have a test account
        cls.utilities.ensure_fresh_account(
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

    @classmethod
    def teardown_class(cls):
        # Clean up our account
        cls.utilities.delete_account(
            account=cls.utilities.test_account_name()
        )

    def test_add_and_delete_role(self):
        cls = type(self)

        # Get an admin
        client_admin = cls.utilities.client_admin()

        # The role does not exist
        nose.tools.assert_false(
            client_admin.has_role(
                account=cls.utilities.test_account_name(),
                role=cls.utilities.test_role()
            )
        )

        nose.tools.assert_not_in(
            cls.utilities.test_role(),
            client_admin.get_roles(
                account=cls.utilities.test_account_name()
            )
        )

        # Add it
        client_admin.add_role(
            account=cls.utilities.test_account_name(),
            role=cls.utilities.test_role()
        )

        # Adding it again fails
        nose.tools.assert_raises(
            Exception,
            client_admin.add_role,
            account=cls.utilities.test_account_name(),
            role=cls.utilities.test_role()
        )

        # The role exists
        nose.tools.assert_true(
            client_admin.has_role(
                account=cls.utilities.test_account_name(),
                role=cls.utilities.test_role()
            )
        )

        nose.tools.assert_in(
            cls.utilities.test_role(),
            client_admin.get_roles(
                account=cls.utilities.test_account_name()
            )
        )

        # Delete it
        client_admin.delete_role(
            account=cls.utilities.test_account_name(),
            role=cls.utilities.test_role()
        )

        # Deleting it again fails
        nose.tools.assert_raises(
            Exception,
            client_admin.delete_role,
            account=cls.utilities.test_account_name(),
            role=cls.utilities.test_role()
        )

        # The role does not exist
        nose.tools.assert_false(
            client_admin.has_role(
                account=cls.utilities.test_account_name(),
                role=cls.utilities.test_role()
            )
        )

        nose.tools.assert_not_in(
            cls.utilities.test_role(),
            client_admin.get_roles(
                account=cls.utilities.test_account_name()
            )
        )
