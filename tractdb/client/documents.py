class TractDBClientDocuments(object):
    def __init__(self, *, client):
        self._client = client

    def _ensure_consistent(self, *, doc, doc_id, doc_rev):
        if doc is None:
            doc = {
                '_id': doc_id,
                '_rev': doc_rev
            }

        if doc_id is None:
            doc_id = doc.get('_id', None)
            if doc_id is None:
                raise Exception('Undefined doc_id.')
        elif '_id' not in doc:
            doc['_id'] = doc_id
        elif doc['_id'] != doc_id:
            raise Exception('Inconsistent doc[\'_id\'] and doc_id.')

        if doc_rev is None:
            doc_rev = doc.get('_rev', None)
            if doc_rev is None:
                raise Exception('Undefined doc_rev.')
        elif '_rev' not in doc:
            doc['_rev'] = doc_rev
        elif doc['_rev'] != doc_rev:
            raise Exception('Inconsistent doc[\'_rev\'] and doc_rev.')

        return doc, doc_id, doc_rev

    def create_document(self, *, doc, doc_id=None):
        """ Create a document.
        """

        # Ensure doc_id and doc['_id'] are consistent
        if doc_id:
            if ('_id' in doc) and (doc_id != doc['_id']):
                raise Exception('Document creation failed.')
        elif '_id' in doc:
            doc_id = doc['_id']

        # Make the post
        if doc_id:
            response = self._client.session.post(
                '{}/{}/{}'.format(
                    self._client.tractdb_url,
                    'document',
                    doc_id
                ),
                json=doc
            )
        else:
            response = self._client.session.post(
                '{}/{}'.format(
                    self._client.tractdb_url,
                    'documents'
                ),
                json={
                    'document': doc
                }
            )

        if response.status_code != 201:
            raise Exception('Document creation failed.')

        # Return the resulting _id and _rev
        json = response.json()

        return {
            '_id': json['_id'],
            '_rev': json['_rev']
        }

    def delete_document(self, *, doc=None, doc_id=None, doc_rev=None):
        """ Delete a document.
        """

        doc, doc_id, doc_rev = self._ensure_consistent(doc=doc, doc_id=doc_id, doc_rev=doc_rev)

        response = self._client.session.delete(
            '{}/{}/{}'.format(
                self._client.tractdb_url,
                'document',
                doc_id
            )
        )

        # TODO: should need to pass doc_rev

        if response.status_code != 200:
            raise Exception('Document deletion failed.')

    def exists_document(self, *, doc_id):
        """ Determine whether a document exists.
        """

        # TODO: this can't be done efficiently without an endpoint

        response = self._client.session.get(
            '{}/{}/{}'.format(
                self._client.tractdb_url,
                'document',
                doc_id
            )
        )

        if response.status_code == 200:
            # Return the resulting _id and _rev
            json = response.json()

            return {
                '_id': json['_id'],
                '_rev': json['_rev']
            }
        else:
            return False

    def get_document(self, *, doc_id):
        """ Get a document.
        """
        response = self._client.session.get(
            '{}/{}/{}'.format(
                self._client.tractdb_url,
                'document',
                doc_id
            )
        )

        if response.status_code != 200:
            raise Exception('Document get failed.')

        return response.json()

    def get_documents(self):
        """ Get a list of documents.
        """
        response = self._client.session.get(
            '{}/{}'.format(
                self._client.tractdb_url,
                'documents'
            )
        )

        if response.status_code != 200:
            raise Exception('Documents get failed.')

        return response.json()['documents']

    def update_document(self, *, doc, doc_id=None, doc_rev=None):
        """ Update a document.
        """

        doc, doc_id, doc_rev = self._ensure_consistent(doc=doc, doc_id=doc_id, doc_rev=doc_rev)

        response = self._client.session.put(
            '{}/{}/{}'.format(
                self._client.tractdb_url,
                'document',
                doc_id
            ),
            json=doc
        )

        if response.status_code != 200:
            raise Exception('Document update failed.')

        # Return the resulting _id and _rev
        json = response.json()

        return {
            '_id': json['_id'],
            '_rev': json['_rev']
        }
