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
        return p.toolkit.render("bpatogalaxy/snippets/bpatogalaxy_send_resource.html")

    def send_package_to_galaxy(self, id):
        print("======================= send_package_to_galaxy ============================== 0")
        context = {
            "model": model,
            "session": model.Session,
            "user": c.user,
            "for_view": True,
            "auth_user_obj": c.userobj,
        }
        print("======================= send_package_to_galaxy ============================== 1")
        data_dict = {"id": id, "include_tracking": True}

        print("======================= send_package_to_galaxy ============================== 2")
        # check if package exists
        try:
            pkg_dict = get_action("package_show")(context, data_dict)
        except (NotFound, NotAuthorized):
            abort(404, _("Dataset not found"))

        print("======================= send_package_to_galaxy ============================== 3")
        name = pkg_dict["name"]

        site_url = config.get("ckan.site_url").rstrip("/")
        query_url = "%s%s" % (
            site_url,
            h.url_for(controller="package", action="read", id=name),
        )
        
        print("======================= send_package_to_galaxy ============================== 4")
        download_url = "%s%s" % (
            site_url,
            h.url_for(controller=self.bpa_ga_controller, action="send_package_to_galaxy", id=id),
        )

        print("======================= send_package_to_galaxy ============================== 5")
        print("======================= send_package_to_galaxy ==============================")
        print("======================= send_package_to_galaxy ==============================")
        print("query_url "+str(query_url))
        print("download_url "+str(download_url))
        print("======================= send_package_to_galaxy ==============================")
        print("======================= send_package_to_galaxy ==============================")
        print("======================= send_package_to_galaxy ==============================")

        return p.toolkit.render("bpatogalaxy/snippets/bpatogalaxy_send_package.html")



