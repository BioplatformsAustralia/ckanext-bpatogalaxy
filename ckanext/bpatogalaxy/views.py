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

from flask import Blueprint

log = logging.getLogger(__name__)
_ = p.toolkit._


bpatogalaxy = Blueprint('bpatogalaxy', __name__)


def index():
    return p.toolkit.render("bpatogalaxy/snippets/bpatogalaxy_send_resource.html")

def send_package_to_galaxy(self, id):
        return p.toolkit.render("bpatogalaxy/snippets/bpatogalaxy_send_package.html")

bpatogalaxy.add_url_rule('/bpatogalaxy', 'index', index)
bpatogalaxy.add_url_rule('/bpatogalaxy/<id>/send_package_to_galaxy', 'send_package_to_galaxy', send_package_to_galaxy)