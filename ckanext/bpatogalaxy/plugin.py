import logging


import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.bpatogalaxy import helpers
from ckanext.bpatogalaxy.views import bpatogalaxy

log = logging.getLogger(__name__)




class BpatogalaxyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint, inherit=True)

     
    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, "static")
        toolkit.add_resource('fanstatic', 'bpatogalaxy')

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.
        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'bpatogalaxy_get_galaxy_workflows_helper': helpers.get_galaxy_workflows,
            'bpatogalaxy_get_galaxy_histories_helper': helpers.get_galaxy_histories,
            'bpatogalaxy_get_galaxy_libraries_helper': helpers.get_galaxy_libraries,
            'bpatogalaxy_get_s3_presigned_url_helper': helpers.send_temp_presigned_url_to_galaxy
        }

    def get_blueprint(self):
        return [bpatogalaxy]

