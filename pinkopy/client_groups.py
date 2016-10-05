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
        groups = data['groups']
        if not groups:
            msg = 'No client groups found in Commvault'
            raise_requests_error(404, msg)
        return groups

    def get_client_properties(self, group_id, xml=False):
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
            return data
            try:
                props = data['clientProperties']
            except KeyError:
                # support previous Commvault api versions
                props = data['App_GetClientPropertiesResponse']['clientProperties']
            if not props:
                msg = 'No client properties found for client {}'.format(client_id)
                raise_requests_error(404, msg)
            return props
