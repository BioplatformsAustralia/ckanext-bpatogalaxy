import logging
import ckan.plugins as p
import ckan.lib.helpers as h
import datetime
import string
from pylons import config
import ckan.lib.base as base

_ = p.toolkit._

log = logging.getLogger(__name__)

class BpatogalaxyController(base.BaseController):
    bpa_ga_controller = "ckanext.bpatogalaxy.controller:BpatogalaxyController"

    def __init__(self, *args, **kwargs):
        super(base.BaseController, self).__init__(*args, **kwargs)
        self.limit = p.toolkit.asint(config.get("ckanext.bulk.limit", 100))

    def index(self):
        return p.toolkit.render("bpatogalaxy/snippets/bpatogalaxy_send_resource_dev_test.html")

    def send_resource_to_galaxy(self, package_id, resource_id):
        print("======================= send_resource_to_galaxy ==============================")
        print(str(package_id))
        print(str(resource_id))
        print("======================= send_resource_to_galaxy ==============================")
        
        return base.render('base_bpatogalaxy/bpatogalaxy_send_resource.html',
                           extra_vars={'package_id': package_id, 'resource_id': resource_id})

    def send_temp_url_to_galaxy(self, url):
        return base.render('base_bpatogalaxy/bpatogalaxy_send_resource.html',
                           extra_vars={'url': url})

