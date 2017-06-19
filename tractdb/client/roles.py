class TractDBClientRoles(object):
    def __init__(self, *, client):
        self._client = client

    def add_role(self, *, account, role):
        """ Add a role.
        """

        response = self._client.session.post(
            '{}/{}/{}/{}'.format(
                self._client.tractdb_url,
                'account',
                account,
                'roles'
            ),
            json={
                'role': role
            }
        )

        if response.status_code != 201:
            raise Exception('Role creation failed.')

    def delete_role(self, *, account, role):
        """ Delete a role.
        """

        response = self._client.session.delete(
            '{}/{}/{}/{}/{}'.format(
                self._client.tractdb_url,
                'account',
                account,
                'role',
                role
            )
        )

        if response.status_code != 200:
            raise Exception('Role deletion failed.')

    def get_roles(self, *, account):
        """ Get an account's roles.
        """

        response = self._client.session.get(
            '{}/{}/{}/{}'.format(
                self._client.tractdb_url,
                'account',
                account,
                'roles'
            )
        )

        if response.status_code != 200:
            raise Exception('Roles get failed.')

        return response.json()['roles']

    def has_role(self, *, account, role):
        """ Determine whether an account has a role.
        """

        # TODO: this can't be done efficiently without an endpoint

        return role in self.get_roles(account=account)

