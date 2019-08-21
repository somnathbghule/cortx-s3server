"""This class provides Key-value REST API i.e. GET,PUT and DELETE."""
import logging
import urllib

from eos_core_client import EOSCoreClient
from eos_get_kv_response import EOSCoreGetKVResponse
from eos_core_error_respose import EOSCoreErrorResponse
from eos_core_success_response import EOSCoreSuccessResponse
from eos_core_util import prepare_signed_header

# EOSCoreKVApi supports key-value REST-API's Put, Get & Delete


class EOSCoreKVApi(EOSCoreClient):
    """EOSCoreKVApi provides key-value REST-API's Put, Get & Delete."""
    _logger = None

    def __init__(self, config, logger=None):
        """Initialise logger and config."""
        if (logger is None):
            self._logger = logging.getLogger("EOSCoreKVApi")
        else:
            self._logger = logger
        self._logger = logging.getLogger()
        self.config = config
        super(EOSCoreKVApi, self).__init__(self.config, logger=self._logger)

    def put(self, index_id=None, object_key_name=None, value=None):
        """Perform PUT request and generate response."""
        if index_id is None:
            self._logger.error("Index Id is required.")
            return None
        if object_key_name is None:
            self._logger.error("Key is required")
            return None

        query_params = ""
        request_body = value

        # The URL quoting functions focus on taking program data and making it safe for use as URL components by quoting special characters and appropriately encoding non-ASCII text.
        # https://docs.python.org/3/library/urllib.parse.html
        # For example if index_id is 'AAAAAAAAAHg=-AwAQAAAAAAA=' and object_key_name is "testobject+"
        # urllib.parse.quote(index_id) and urllib.parse.quote(object_key_name) yields 'testobject%2B' respectively
        # And request_uri is
        # '/indexes/AAAAAAAAAHg%3D-AwAQAAAAAAA%3D/testobject%2B'

        request_uri = '/indexes/' + \
            urllib.parse.quote(index_id) + '/' + \
            urllib.parse.quote(object_key_name)
        headers = prepare_signed_header(
            'PUT', request_uri, query_params, request_body)

        if(headers['Authorization'] is None):
            self._logger.error("Failed to generate v4 signature")
            return None

        try:
            response = super(
                EOSCoreKVApi,
                self).put(
                request_uri,
                request_body,
                headers=headers)
        except Exception as ex:
            self._logger.error(str(ex))
            return None

        if response['status'] == 201:
            self._logger.info("Key value details added successfully.")
            return True, EOSCoreSuccessResponse(response['body'])
        else:
            self._logger.info('Failed to add key value details.')
            return False, EOSCoreErrorResponse(
                response['status'], response['reason'], response['body'])

    def get(self, index_id=None, object_key_name=None):
        """Perform GET request and generate response."""
        if index_id is None:
            self._logger.error("Index Id is required.")
            return None
        if object_key_name is None:
            self._logger.error("Key is required")
            return None

        # The URL quoting functions focus on taking program data and making it safe for use as URL components by quoting special characters and appropriately encoding non-ASCII text.
        # https://docs.python.org/3/library/urllib.parse.html
        # For example if index_id is 'AAAAAAAAAHg=-AwAQAAAAAAA=' and object_key_name is "testobject+"
        # urllib.parse.quote(index_id) and urllib.parse.quote(object_key_name) yields 'testobject%2B' respectively
        # And request_uri is
        # '/indexes/AAAAAAAAAHg%3D-AwAQAAAAAAA%3D/testobject%2B'

        request_uri = '/indexes/' + \
            urllib.parse.quote(index_id) + '/' + \
            urllib.parse.quote(object_key_name)

        query_params = ""
        body = ""
        headers = prepare_signed_header('GET', request_uri, query_params, body)

        if(headers['Authorization'] is None):
            self._logger.error("Failed to generate v4 signature")
            return None

        try:
            response = super(
                EOSCoreKVApi,
                self).get(
                request_uri,
                headers=headers)
        except Exception as ex:
            self._logger.error(str(ex))
            return None

        if response['status'] == 200:
            self._logger.info("Get kv operation successfully.")
            return True, EOSCoreGetKVResponse(
                object_key_name, response['body'])
        else:
            self._logger.info('Failed to get kv details.')
            return False, EOSCoreErrorResponse(
                response['status'], response['reason'], response['body'])

    def delete(self, index_id=None, object_key_name=None):
        """Perform DELETE request and generate response."""
        if index_id is None:
            self._logger.error("Index Id is required.")
            return None
        if object_key_name is None:
            self._logger.error("Key is required")
            return None

        # The URL quoting functions focus on taking program data and making it safe for use as URL components by quoting special characters and appropriately encoding non-ASCII text.
        # https://docs.python.org/3/library/urllib.parse.html
        # For example if index_id is 'AAAAAAAAAHg=-AwAQAAAAAAA=' and object_key_name is "testobject+"
        # urllib.parse.quote(index_id) and urllib.parse.quote(object_key_name) yields 'testobject%2B' respectively
        # And request_uri is
        # '/indexes/AAAAAAAAAHg%3D-AwAQAAAAAAA%3D/testobject%2B'

        request_uri = '/indexes/' + \
            urllib.parse.quote(index_id) + '/' + \
            urllib.parse.quote(object_key_name)

        body = ""
        query_params = ""
        headers = prepare_signed_header(
            'DELETE', request_uri, query_params, body)

        if(headers['Authorization'] is None):
            self._logger.error("Failed to generate v4 signature")
            return None

        try:
            response = super(
                EOSCoreKVApi,
                self).delete(
                request_uri,
                headers=headers)
        except Exception as ex:
            self._logger.error(str(ex))
            return None

        if response['status'] == 204:
            self._logger.info('Key value deleted.')
            return True, EOSCoreSuccessResponse(response['body'])
        else:
            self._logger.info('Failed to delete key value.')
            return False, EOSCoreErrorResponse(
                response['status'], response['reason'], response['body'])