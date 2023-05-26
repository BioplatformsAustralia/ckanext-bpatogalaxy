import logging
import ckan.lib.helpers as h
from ckan.plugins import toolkit as tk
from ckanext.bpatogalaxy import helpers as helpers
from flask import Blueprint

log = logging.getLogger(__name__)


bpatogalaxy = Blueprint('bpatogalaxy', __name__, url_prefix=u'/dataset/<id>/resource')


def send_package_to_galaxy(id, resource_id):
    resource = tk.get_action('resource_show')({'ignore_auth':True}, {'id': resource_id})
    if not resource:
        h.flash_error("Resource not found")
        return tk.redirect_to(tk.url_for('dataset.read', id=id))
    try:
        result = helpers.send_temp_presigned_url_to_galaxy(resource_id, resource.get('name'))
    except Exception as e:
        log.error(e)
        h.flash_error(e)
        return tk.redirect_to(tk.url_for('dataset.read', id=id))
    if not result:
        h.flash_success("Package sent to Galaxy")    
    else:
        h.flash_error("Error sending package to Galaxy")
        
    return tk.redirect_to(tk.url_for('dataset.read', id=id))


bpatogalaxy.add_url_rule('/<resource_id>/send_package_to_galaxy',
                        view_func=send_package_to_galaxy)