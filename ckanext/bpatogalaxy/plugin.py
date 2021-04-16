import logging
import pylons

#import ckanapi
import urllib2
import urllib
import json
import pprint

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model
from ckan.plugins import IPackageController
from bioblend.galaxy import GalaxyInstance

log = logging.getLogger(__name__)


def get_galaxy_workflows():
    print("Initiating Galaxy connection")

    gi = GalaxyInstance(url="", key="")

    print("Retrieving Workflows list")

    workflows = gi.workflows.get_workflows()

    if len(workflows) == 0:
        print("There are no Workflows in your account.")
    else:
        print("\nWorkflows:")
        for wf_dict in workflows:
            print("{} : {}".format(wf_dict['name'], wf_dict['id']))

    return workflows


class BpatogalaxyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def before_map(self, map):
        bpa_ga_controller = "ckanext.bpatogalaxy.controller:BpatogalaxyController"
        map.connect(
            "bpatogalaxy", 
            "/bpatogalaxy",
            controller=bpa_ga_controller, 
            action="index"
        )
        return map

    def after_map(self, map):
        return map
    
    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'bpatogalaxy_get_galaxy_workflows_helper': get_galaxy_workflows}

