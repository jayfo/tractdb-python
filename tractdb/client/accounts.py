class TractDBClientAccounts(object):
    def __init__(self, *, client):
        self._client = client

    def create_account(self, *, account, password):
        """ Create an account.
        """

        response = self._client.session.post(
            '{}/{}'.format(
                self._client.tractdb_url,
                'accounts'
            ),
            json={
                'account': account,
                'password': password
            }
        )

        if response.status_code != 201:
            raise Exception('Account creation failed.')

    def delete_account(self, *, account):
        """ Delete an account.
        """

        response = self._client.session.delete(
            '{}/{}/{}'.format(
                self._client.tractdb_url,
                'account',
                account
            )
        )

        if response.status_code != 200:
            raise Exception('Account deletion failed.')

    def exists_account(self, *, account):
        """ Determine whether an account exists.
        """

        # TODO: this can't be done efficiently without an endpoint

        return account in self.get_accounts()

    def get_accounts(self):
        """ Get a list of accounts.
        """

        response = self._client.session.get(
            '{}/{}'.format(
                self._client.tractdb_url,
                'accounts'
            )
        )

        if response.status_code != 200:
            raise Exception('Accounts get failed.')

        return response.json()['accounts']
