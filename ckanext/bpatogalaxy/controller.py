import logging
import ckan.plugins as p
import ckan.lib.helpers as h
import datetime
import string
from ckan.common import request, c
from pylons import config
from ckan import model
from ckan.lib.base import abort, BaseController
from ckan.logic import NotFound, NotAuthorized, get_action, check_access

_ = p.toolkit._


log = logging.getLogger(__name__)


class BpatogalaxyController(BaseController):
    bpa_ga_controller = "ckanext.bpatogalaxy.controller:BpatogalaxyController"

    def __init__(self, *args, **kwargs):
        super(BaseController, self).__init__(*args, **kwargs)
        self.limit = p.toolkit.asint(config.get("ckanext.bulk.limit", 100))

    def index(self):
        return p.toolkit.render("bpatogalaxy/snippets/bpatogalaxy.html")


