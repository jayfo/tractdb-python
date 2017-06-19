import inspect
import requests
import tractdb.client.accounts
import tractdb.client.documents
import tractdb.client.roles


class TractDBClient(object):
    """ Client for interacting with a TractDB instance.
    """

    def __init__(self, *, tractdb_url, account, password):
        """ Create a client.
        """
        self._tractdb_url = tractdb_url
        self._account = account
        self._password = password

        self._session = self._create_session(account=account, password=password)

        services = [
            tractdb.client.accounts.TractDBClientAccounts(client=self),
            tractdb.client.documents.TractDBClientDocuments(client=self),
            tractdb.client.roles.TractDBClientRoles(client=self),
        ]
        for service in services:
            for name, method in inspect.getmembers(service):
                if not name.startswith('_'):
                    self.__setattr__(name, method)

    def _create_session(self, *, account, password):
        """ Initialize a session for use within a client.
        """

        session = requests.Session()

        response = session.post(
            '{}/{}'.format(
                self._tractdb_url,
                'login'
            ),
            json={
                'account': account,
                'password': password
            }
        )

        if response.status_code != 200:
            raise Exception('Session creation failed.')

        return session

    @property
    def session(self):
        return self._session

    @property
    def tractdb_url(self):
        return self._tractdb_url
