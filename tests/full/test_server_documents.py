import base.docker.docker_commands
import tractdb.server.accounts
import tractdb.server.documents
import unittest


TEST_ACCOUNT = 'test-account'
TEST_ACCOUNT_PASSWORD = 'test-account-password'
TEST_DOC_ID = 'docid_test'
TEST_CONTENT = {
    'user_id': '001',
    'text': 'some content',
    'date': '03/20/2017'
}
TEST_UPDATED_CONTENT = {
    'user_id': '001',
    'text': 'some new content added',
    'date': '03/20/2017'
}
TEST_UPDATED_AGAIN_CONTENT = {
    'user_id': '001',
    'text': 'some newest content added',
    'date': '03/20/2017'
}


def setup():
    pass


def teardown():
    pass


class TestServerDocuments(unittest.TestCase):
    @property
    def accountAdmin(self):
        return tractdb.server.accounts.AccountsAdmin(
            couchdb_url='http://{}:5984'.format(
                base.docker.docker_commands.machine_ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    @property
    def documentAdmin(self):
        return tractdb.server.documents.DocumentsAdmin(
            couchdb_url='http://{}:5984'.format(
                base.docker.docker_commands.machine_ip()
            ),
            couchdb_user=TEST_ACCOUNT,
            couchdb_user_password=TEST_ACCOUNT_PASSWORD
        )

    def setUp(self):
        if TEST_ACCOUNT not in self.accountAdmin.list_accounts():
            self.accountAdmin.create_account(TEST_ACCOUNT, TEST_ACCOUNT_PASSWORD)

    def tearDown(self):
        if TEST_ACCOUNT in self.accountAdmin.list_accounts():
            self.accountAdmin.delete_account(TEST_ACCOUNT)

    def test_create_get_delete_document(self):
        self.assertNotIn(
            TEST_DOC_ID,
            self.documentAdmin.list_documents()
        )

        self.assertFalse(
            self.documentAdmin.exists_document(TEST_DOC_ID)
        )

        result = self.documentAdmin.create_document(
            TEST_CONTENT,
            TEST_DOC_ID
        )
        doc_id = result['id']
        self.assertEquals(doc_id, TEST_DOC_ID)

        self.assertIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        self.assertTrue(
            self.documentAdmin.exists_document(TEST_DOC_ID)
        )

        doc = self.documentAdmin.get_document(doc_id)

        self.assertIsInstance(
            doc,
            dict
        )

        # Remove the internal fields for comparison
        del doc['_id']
        del doc['_rev']

        self.assertEqual(
            doc,
            TEST_CONTENT
        )

        self.documentAdmin.delete_document(
            doc_id
        )

        self.assertNotIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        self.assertFalse(
            self.documentAdmin.exists_document(TEST_DOC_ID)
        )

    def test_create_document_id_conflict(self):
        # create a document with an _id that already exists, confirm the attempted duplication fails
        self.assertNotIn(
            TEST_DOC_ID,
            self.documentAdmin.list_documents()
        )

        result = self.documentAdmin.create_document(
            TEST_CONTENT,
            TEST_DOC_ID
        )
        doc_id = result['id']

        self.assertIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        with self.assertRaises(Exception):
            self.documentAdmin.create_document(
                TEST_CONTENT,
                TEST_DOC_ID
            )

        self.documentAdmin.delete_document(
            doc_id
        )

    def test_create_document_id_known(self):
        # create a document by assigning an _id, see that couch does use that _id
        self.assertNotIn(
            TEST_DOC_ID,
            self.documentAdmin.list_documents()
        )

        result = self.documentAdmin.create_document(
            TEST_CONTENT,
            doc_id=TEST_DOC_ID
        )
        doc_id = result['id']

        self.assertEquals(
            doc_id,
            TEST_DOC_ID
        )

        self.assertIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        self.documentAdmin.delete_document(
            doc_id
        )

    def test_create_document_id_unknown(self):
        # create a document without assigning it an _id, see that couch assigns one
        result = self.documentAdmin.create_document(
            TEST_CONTENT
        )
        doc_id = result['id']

        self.assertIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        self.documentAdmin.delete_document(
            doc_id
        )

        self.assertNotIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

    def test_create_get_update_get_document(self):
        # Create it
        result = self.documentAdmin.create_document(
            TEST_CONTENT
        )
        doc_id = result['id']

        # Confirm created
        self.assertIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        # Read it
        doc = self.documentAdmin.get_document(
            doc_id
        )

        # Create an updated document
        doc_updated = dict(doc)
        doc_updated.update(TEST_UPDATED_CONTENT)

        # Remove the internal fields for comparison
        del doc['_id']
        del doc['_rev']

        # Ensure we get the right content
        self.assertEquals(
            doc,
            TEST_CONTENT
        )

        # Update it
        self.documentAdmin.update_document(
            doc_updated
        )

        # Ensure we get the new content
        doc_updated = self.documentAdmin.get_document(
            doc_id
        )

        # Remove the internal fields for comparison
        del doc_updated['_id']
        del doc_updated['_rev']

        self.assertEquals(
            doc_updated,
            TEST_UPDATED_CONTENT
        )

        # Delete it
        self.documentAdmin.delete_document(
            doc_id
        )

        # Ensure it's gone
        self.assertNotIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

    def test_list_documents(self):
        self.assertIsInstance(
            self.documentAdmin.list_documents(),
            list
        )

    def test_update_document_conflict(self):
        # update a document, create a conflict error, confirm that happens
        # this will require
        #  - make a document, it has an _id and a _rev
        #  - copy that document (so you keep the _rev)
        #  - modify and update the document (this should succeed and give you a new _rev)
        #  - using a the copy, modify and update again (this should fail, the _rev doesn't match anymore)

        # Create it
        result = self.documentAdmin.create_document(
            TEST_CONTENT,
            TEST_DOC_ID
        )
        doc_id = result['id']

        # Confirm created
        self.assertIn(
            doc_id,
            self.documentAdmin.list_documents()
        )

        # Read it
        doc = self.documentAdmin.get_document(
            doc_id
        )

        # Create an updated document
        doc_updated = dict(doc)
        doc_updated.update(TEST_UPDATED_CONTENT)

        # Update it
        self.documentAdmin.update_document(
            doc_updated
        )

        # Ensure we get the new content
        doc_updated = self.documentAdmin.get_document(
            doc_id
        )

        # Remove the internal fields for comparison
        del doc_updated['_id']
        del doc_updated['_rev']

        self.assertEquals(
            doc_updated,
            TEST_UPDATED_CONTENT
        )

        # Create another updated document from the origin doc with invalid rev
        doc_updated_again = dict(doc)
        doc_updated_again.update(TEST_UPDATED_AGAIN_CONTENT)

        with self.assertRaises(Exception):
            # Update it
            self.documentAdmin.update_document(
                doc_updated_again
            )

        # Delete it
        self.documentAdmin.delete_document(
            doc_id
        )

    def test_update_document_parameters(self):
        # Create it
        result = self.documentAdmin.create_document(
            TEST_CONTENT,
            TEST_DOC_ID
        )
        doc_id = result['id']
        doc_rev = result['rev']

        # Read it
        doc = self.documentAdmin.get_document(
            doc_id
        )

        # Create an updated document
        doc_updated = dict(doc)
        doc_updated.update(TEST_UPDATED_CONTENT)

        # Update it with a mismatched '_id' vs doc_id, should fail
        with self.assertRaises(Exception):
            self.documentAdmin.update_document(
                doc_updated,
                doc_id='wrong'
            )

        # Update it with a mismatched '_rev' vs doc_rev, should fail
        with self.assertRaises(Exception):
            self.documentAdmin.update_document(
                doc_updated,
                doc_rev='wrong'
            )

        # Remove the internal fields and update using our parameters
        del doc_updated['_id']
        del doc_updated['_rev']

        self.documentAdmin.update_document(
            doc_updated,
            doc_id=doc_id,
            doc_rev=doc_rev
        )

        # Delete it
        self.documentAdmin.delete_document(
            doc_id
        )
