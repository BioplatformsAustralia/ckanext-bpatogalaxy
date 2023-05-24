import logging
import ckan.plugins as p
import ckan.lib.helpers as h


from flask import Blueprint

log = logging.getLogger(__name__)
_ = p.toolkit._


bpatogalaxy = Blueprint('bpatogalaxy', __name__)


def index():
    return p.toolkit.render("snippets/bpatogalaxy_send_resource.html")

def send_package_to_galaxy(id):
        return p.toolkit.render("bpatogalaxy/snippets/download_window_link_bpatogalaxy.html")

bpatogalaxy.add_url_rule('/bpatogalaxy', 'index', index)
bpatogalaxy.add_url_rule('/bpatogalaxy/<id>/send_package_to_galaxy', 'send_package_to_galaxy', send_package_to_galaxy)