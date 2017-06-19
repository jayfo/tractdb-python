import nose.tools
import tests.utilities
import tractdb.client


class TestClientDocuments:
    @classmethod
    def setup_class(cls):
        cls.utilities = tests.utilities.Utilities(cls)

        # Ensure we have a test account
        cls.utilities.ensure_fresh_account(
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

        # Ensure we have a client for the account
        cls.client = tractdb.client.TractDBClient(
            tractdb_url=cls.utilities.url_base_pyramid(),
            account=cls.utilities.test_account_name(),
            password=cls.utilities.test_account_password()
        )

    @classmethod
    def teardown_class(cls):
        # Clean up our account
        cls.utilities.delete_account(
            account=cls.utilities.test_account_name()
        )

    def setup(self):
        cls = type(self)

        # Ensure no documents remain from prior tests
        cls.utilities.delete_all_documents(client=cls.client)

    def teardown(self):
        cls = type(self)

        # Clean up our documents
        cls.utilities.delete_all_documents(client=cls.client)

    def test_create_get_delete_document(self):
        cls = type(self)
        client = cls.client

        # The document we will create/get/delete
        doc = cls.utilities.test_document()
        doc_id = cls.utilities.test_document_id()

        # The document does not exist
        nose.tools.assert_false(
            client.exists_document(
                doc_id=doc_id
            )
        )

        nose.tools.assert_not_in(
            doc_id,
            [doc['_id'] for doc in client.get_documents()]
        )

        # Create it, store resulting _id and _rev
        doc.update(
            client.create_document(
                doc=doc,
                doc_id=doc_id
            )
        )
        nose.tools.assert_in('_id', doc)
        nose.tools.assert_in('_rev', doc)

        # TODO: the server isn't enforcing this

        # # Creating again should fail, because the id already exists
        # nose.tools.assert_raises(
        #     Exception,
        #     client.create_document,
        #     doc=doc,
        #     doc_id=doc_id
        # )

        # The document exists
        nose.tools.assert_true(
            client.exists_document(
                doc_id=doc_id
            )
        )

        nose.tools.assert_in(
            doc_id,
            [doc['_id'] for doc in client.get_documents()]
        )

        # Get the document, see that it matches what we made
        doc_retrieved = client.get_document(doc_id=doc_id)
        nose.tools.assert_equal(
            doc,
            doc_retrieved
        )

        # Delete the document
        client.delete_document(doc=doc)

        # Deleting it again fails
        nose.tools.assert_raises(
            Exception,
            client.delete_document,
            doc=doc,
        )

        # The document does not exist
        nose.tools.assert_false(
            client.exists_document(
                doc_id=doc_id
            )
        )

        nose.tools.assert_not_in(
            doc_id,
            [doc['_id'] for doc in client.get_documents()]
        )

    # def test_create_document_id_conflict(self):
    #     # create a document with an _id that already exists, confirm the attempted duplication fails
    #     self.assertNotIn(
    #         TEST_DOC_ID,
    #         self.client_admin.list_documents()
    #     )
    #
    #     result = self.client_admin.create_document(
    #         TEST_CONTENT,
    #         TEST_DOC_ID
    #     )
    #     doc_id = result['id']
    #
    #     self.assertIn(
    #         doc_id,
    #         self.client_admin.list_documents()
    #     )
    #
    #     with self.assertRaises(Exception):
    #         self.client_admin.create_document(
    #             TEST_CONTENT,
    #             TEST_DOC_ID
    #         )
    #
    #     self.client_admin.delete_document(
    #         doc_id
    #     )
    #
    # def test_create_document_id_known(self):
    #     # create a document by assigning an _id, see that couch does use that _id
    #     self.assertNotIn(
    #         TEST_DOC_ID,
    #         self.client_admin.list_documents()
    #     )
    #
    #     result = self.client_admin.create_document(
    #         TEST_CONTENT,
    #         doc_id=TEST_DOC_ID
    #     )
    #     doc_id = result['id']
    #
    #     self.assertEquals(
    #         doc_id,
    #         TEST_DOC_ID
    #     )
    #
    #     self.assertIn(
    #         doc_id,
    #         self.client_admin.list_documents()
    #     )
    #
    #     self.client_admin.delete_document(
    #         doc_id
    #     )
    #
    # def test_create_document_id_unknown(self):
    #     # create a document without assigning it an _id, see that couch assigns one
    #     result = self.client_admin.create_document(
    #         TEST_CONTENT
    #     )
    #     doc_id = result['id']
    #
    #     self.assertIn(
    #         doc_id,
    #         self.client_admin.list_documents()
    #     )
    #
    #     self.client_admin.delete_document(
    #         doc_id
    #     )
    #
    #     self.assertNotIn(
    #         doc_id,
    #         self.client_admin.list_documents()
    #     )

    def test_create_update_get_document(self):
        cls = type(self)
        client = cls.client

        # The document will create/modify/get
        doc = cls.utilities.test_document()
        doc_id = cls.utilities.test_document_id()

        # Create it, store resulting _id and _rev
        doc.update(
            client.create_document(
                doc=doc,
                doc_id=doc_id
            )
        )
        nose.tools.assert_in('_id', doc)
        nose.tools.assert_in('_rev', doc)

        # Modify it
        doc_modified = dict(doc)
        doc_modified.update(cls.utilities.test_document(document_index=1))

        doc_modified.update(
            client.update_document(
                doc=doc_modified,
                doc_id=doc['_id'],
                doc_rev=doc['_rev']
            )
        )

        # Get the modified document
        doc_retrieved = client.get_document(doc_id=doc_id)

        # Ensure they are the same
        nose.tools.assert_equal(
            doc_retrieved,
            doc_modified
        )

        # And actually modified versus our original
        nose.tools.assert_not_equal(
            doc_retrieved,
            doc
        )

    # def test_list_documents(self):
    #     self.assertIsInstance(
    #         self.client_admin.list_documents(),
    #         list
    #     )
    #
    # def test_update_document_conflict(self):
    #     # update a document, create a conflict error, confirm that happens
    #     # this will require
    #     #  - make a document, it has an _id and a _rev
    #     #  - copy that document (so you keep the _rev)
    #     #  - modify and update the document (this should succeed and give you a new _rev)
    #     #  - using a the copy, modify and update again (this should fail, the _rev doesn't match anymore)
    #
    #     # Create it
    #     result = self.client_admin.create_document(
    #         TEST_CONTENT,
    #         TEST_DOC_ID
    #     )
    #     doc_id = result['id']
    #
    #     # Confirm created
    #     self.assertIn(
    #         doc_id,
    #         self.client_admin.list_documents()
    #     )
    #
    #     # Read it
    #     doc = self.client_admin.get_document(
    #         doc_id
    #     )
    #
    #     # Create an updated document
    #     doc_updated = dict(doc)
    #     doc_updated.update(TEST_UPDATED_CONTENT)
    #
    #     # Update it
    #     self.client_admin.update_document(
    #         doc_updated
    #     )
    #
    #     # Ensure we get the new content
    #     doc_updated = self.client_admin.get_document(
    #         doc_id
    #     )
    #
    #     # Remove the internal fields for comparison
    #     del doc_updated['_id']
    #     del doc_updated['_rev']
    #
    #     self.assertEquals(
    #         doc_updated,
    #         TEST_UPDATED_CONTENT
    #     )
    #
    #     # Create another updated document from the origin doc with invalid rev
    #     doc_updated_again = dict(doc)
    #     doc_updated_again.update(TEST_UPDATED_AGAIN_CONTENT)
    #
    #     with self.assertRaises(Exception):
    #         # Update it
    #         self.client_admin.update_document(
    #             doc_updated_again
    #         )
    #
    #     # Delete it
    #     self.client_admin.delete_document(
    #         doc_id
    #     )
