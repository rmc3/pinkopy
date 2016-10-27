import logging
import xmltodict
from dicttoxml import dicttoxml

from .base_session import BaseSession
from .exceptions import raise_requests_error

log = logging.getLogger(__name__)


class SchedulesSession(BaseSession):
    """Methods for schedules."""
    def __init__(self, cache_methods=None, *args, **kwargs):
        cache_methods = cache_methods or ['get_schedules']
        super(SchedulesSession, self).__init__(cache_methods=cache_methods, *args, **kwargs)

    def get_schedules(self, clientId=None, apptypeId=None, instanceId=None, backupsetId=None, subclientId=None):
        """Get schedules.

        Returns:
            list: schedules
        """
        path = 'Schedules'
        qstr_vals = {
            "clientId": clientId,
            "apptypeId": apptypeId,
            "instanceId": instanceId,
            "backupsetId": backupsetId,
            "subclientId": subclientId
        }
        for key in qstr_vals.keys():
            if qstr_vals[key] == None:
                qstr_vals.pop(key)
        res = self.request('GET', path, qstr_vals=qstr_vals)
        data = res.json()
        return data
