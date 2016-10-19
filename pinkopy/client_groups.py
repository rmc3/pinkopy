import logging
import xmltodict
from dicttoxml import dicttoxml

from .base_session import BaseSession
from .exceptions import raise_requests_error

log = logging.getLogger(__name__)


class ClientGroupSession(BaseSession):
    """Methods for client groups."""
    def __init__(self, cache_methods=None, *args, **kwargs):
        cache_methods = cache_methods or ['get_client_groups',
                                          'get_client_group_properties',
                                          'get_client_group']
        super(ClientGroupSession, self).__init__(cache_methods=cache_methods, *args, **kwargs)

    def get_client_groups(self):
        """Get clients.

        Returns:
            list: clients
        """
        path = 'ClientGroup'
        res = self.request('GET', path)
        data = res.json()
        if not 'groups' in data:
            groups = []
        else:
            groups = data['groups']
        return groups

    def get_client_group_properties(self, group_id, xml=False):
        """Get client group properties.

        This call sometimes replies in XML, because who cares about
        Accept headers right. So, we must take the reply in XML and
        convert it to JSON to maintain sanity.

        Args:
            group_id (str): client group ID
            xml (boolean): If True, returns the raw XML response.

        Returns:
            dict: client group properties
        """
        if isinstance(group_id, int):
            log.warning('deprecated: group_id support for int for backward compatibility only')
            group_id = str(group_id)
        path = 'ClientGroup/{}'.format(group_id)
        if xml:
            headers = {"Accept": "application/xml"}
        else:
            headers = {}
        res = self.request('GET', path, headers=headers)
        # If you are using a < v10 SP12 this call will respond in
        # xml even though we are requesting json.
        if xml:
            return res.text
        else:
            if not res.json():
                # turn wrong xml into json
                data = xmltodict.parse(res.text)
            else:
                data = res.json()
            try:
                props = data['clientGroupDetail']
            except KeyError:
                # support previous Commvault api versions
                props = data['App_PerformClientGroupResp']['clientGroupDetail']
            if not props:
                msg = 'No client properties found for client group {}'.format(client_id)
                raise_requests_error(404, msg)
            return props


    def post_client_group(self, props):
        """Create a new client group

        Args:
            props (str): XML client group properties string

        Returns:
            dict: response
        """
        path = 'ClientGroup'
        res = self.request('POST', path, payload_nondict=props, headers={"Content-type": "application/xml"})
        if not res.json():
            data = xmltodict.parse(res.text)
        else:
            data = res.json()
        return data['clientGroupDetail']

    def post_client_group_properties(self, client_group_id, props):
        """Post client group properties.

        Args:
            client_group_id (str): client group id
            props (str): XML subclient properties string

        Returns:
            dict: response
        """
        if isinstance(client_group_id, int):
            log.warning('deprecated: subclient_id support for int for backward compatibility only')
            client_group_id = str(client_group_id)
        path = 'ClientGroup/{}'.format(client_group_id)
        res = self.request('POST', path, payload_nondict=props, headers={"Content-type": "application/xml"})
        if not res.json():
            data = xmltodict.parse(res.text)
        else:
            data = res.json()
        return data
