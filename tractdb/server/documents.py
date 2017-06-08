import couchdb
import re
import urllib.parse


class DocumentsAdmin(object):
    """ Supports management of TractDB documents.
    """

    def __init__(self, couchdb_url, couchdb_user, couchdb_user_password):
        """ Create an admin object.
        """
        self._couchdb_url = couchdb_url
        self._couchdb_user = couchdb_user
        self._couchdb_user_password = couchdb_user_password

    def create_document(self, doc, doc_id=None):
        """ Add a document to a database.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        # Get the database for the user
        database = server[dbname]

        # Ensure we have 'just' a dictionary
        doc = dict(doc)

        # If we were told what id to use, use it
        if doc_id:
            doc['_id'] = doc_id

        # Store the document
        created_id, created_rev = database.save(doc)

        return {
            'id': created_id,
            'rev': created_rev
        }

    def exists_document(self, doc_id):
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Check whether the document exists
        return doc_id in database

    def get_document(self, doc_id):
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        doc = database[doc_id]

        # Return as a dict, not our CouchDB internal object
        return dict(doc)

    def update_document(self, doc, doc_id=None, doc_rev=None):
        """ Update a doc.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Must provide either '_id' or doc_id, if both they need to match
        if '_id' in doc:
            if doc_id is not None:
                if doc_id != doc['_id']:
                    raise Exception(
                        'Mismatched parameters doc[\'_id\']="{:s}" and doc_id="{:s}"'.format(
                            doc['_id'],
                            doc_id
                        )
                    )
        else:
            if doc_id is None:
                raise Exception(
                    'Missing parameter doc[\'_id\'] or doc_id'
                )

            doc = dict(doc)
            doc['_id'] = doc_id

        # Must provide either '_rev' or doc_rev, if both they need to match
        if '_rev' in doc:
            if doc_rev is not None:
                if doc_rev != doc['_rev']:
                    raise Exception(
                        'Mismatched parameters doc[\'_rev\']="{:s}" and doc_rev="{:s}"'.format(
                            doc['_rev'],
                            doc_id
                        )
                    )
        else:
            if doc_rev is None:
                raise Exception(
                    'Missing parameter doc[\'_rev\'] or doc_rev'
                )

            doc = dict(doc)
            doc['_rev'] = doc_rev

        # Update the document
        try:
            new_doc_id, new_doc_rev = database.save(doc)
        except couchdb.http.ResourceConflict:
            raise Exception('Revision conflict for document "{:s}".'.format(doc['_id']))

        return {
            'id': new_doc_id,
            'rev': new_doc_rev
        }

    def delete_document(self, doc_id):
        """ Delete a doc.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        # Delete it
        del database[doc_id]

    def list_documents(self):
        """ List the id of all the documents of the given account.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(self._couchdb_user)
        dbname = '{:s}_tractdb'.format(self._couchdb_user)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(self._couchdb_user))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Return all document ids
        return [doc for doc in database]

    def _format_server_url(self):
        """ Format the base URL we use for connecting to the server.
        """
        return '{}://{:s}:{:s}@{:s}'.format(
            urllib.parse.urlparse(self._couchdb_url).scheme,
            self._couchdb_user,
            self._couchdb_user_password,
            self._couchdb_url[
                len(urllib.parse.urlparse(self._couchdb_url).scheme) + len('://')
                :
            ]
        )

    @property
    def _couchdb_databases(self):
        """ List what CouchDB databases exist.
        """
        server = self._couchdb_server

        # Our databases are defined by the user name plus the suffix '_tractdb'
        pattern = re.compile('.*_tractdb')
        dbnames = [dbname for dbname in server if pattern.match(dbname)]

        return dbnames

    @property
    def _couchdb_users(self):
        """ List what CouchDB users exist.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']

        # This is our docid pattern
        pattern = re.compile('org\.couchdb\.user:(.*)')

        # Keep only the users that match our pattern, extracting the user
        users = []
        for docid in database_users:
            match = pattern.match(docid)
            if match:
                account_user = match.group(1)
                users.append(account_user)

        return users

    @property
    def _couchdb_server(self):
        return couchdb.Server(self._format_server_url())
