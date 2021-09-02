import logging
import pylons

import urllib2
import urllib
import json
import pprint

import boto3
from ckantoolkit import config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model
from ckan.plugins import IPackageController
from bioblend.galaxy import GalaxyInstance

log = logging.getLogger(__name__)


def get_galaxy_workflows():
    print("Initiating Galaxy connection")
    galaxy_host = config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = config.get('ckanext.bpatogalaxy.galaxy_api_key')

    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)

    print("Retrieving Workflows list")

    workflows = gi.workflows.get_workflows()

    if len(workflows) == 0:
        print("There are no Workflows in your account.")
    else:
        print("\nWorkflows:")
        for wf_dict in workflows:
            print("{} : {}".format(wf_dict['name'], wf_dict['id']))

    return workflows


def get_galaxy_histories():
    print("Initiating Galaxy connection")
    galaxy_host = config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = config.get('ckanext.bpatogalaxy.galaxy_api_key')

    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)

    print("Retrieving Histories list")

    histories = gi.histories.get_histories()

    if len(histories) == 0:
        print("There are no Histories in your account.")
    else:
        print("\nHistories:")
        for hist_dict in histories:
            # As an example, we retrieve a piece of metadata (the size) using show_history
            hist_details = gi.histories.show_history(hist_dict['id'])
            print("{} ({}) : {}".format(hist_dict['name'], hist_details['size'], hist_dict['id']))

    return histories


def get_galaxy_libraries():
    print("Initiating Galaxy connection")
    galaxy_host = config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = config.get('ckanext.bpatogalaxy.galaxy_api_key')

    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)

    print("Retrieving Libraries list")

    libraries = gi.libraries.get_libraries()

    if len(libraries) == 0:
        print("There are no Data Libraries available.")
        gi.libraries.create_library('TestLibraryAPI','Test Library Created From The API', 'Test Library Created From The API')
    else:
        print("\nData Libraries:")
        for lib_dict in libraries:
            print("{} : {}".format(lib_dict['name'], lib_dict['id']))

    return libraries


def get_s3_presigned_url():
    bucket_path = config.get('ckanext.s3filestore.aws_storage_path')
    bpa_resource_url = bucket_path +  config.get('ckanext.bpatogalaxy.galaxy_test_file')
    galaxy_host = config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = config.get('ckanext.bpatogalaxy.galaxy_api_key')
    token_key = config.get('ckanext.bpatogalaxy.ckan_api_key')
    token_name= config.get('ckanext.bpatogalaxy.ckan_api_key_name')
    
    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)

    histories = gi.histories.get_histories()

    url = bpa_resource_url

    if len(histories) >= 0:
        print("Uploading from history to url")
        gi.histories.upload_history_from_url(url=url,token_name=token_name,token_key=token_key)
    else:
        print("\nDo nothing!!!")

    return url


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
        bpa_ga_pkg_controller = "ckanext.bpatogalaxy.controller:BpatogalaxyController"
        map.connect(
            "bpatogalaxy_send_package",
            "/bpatogalaxy/{id}/send_package_to_galaxy",
            action="send_package_to_galaxy",
            controller=bpa_ga_pkg_controller,
        )
        return map

    def after_map(self, map):
        return map
    
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
            'bpatogalaxy_get_galaxy_workflows_helper': get_galaxy_workflows,
            'bpatogalaxy_get_galaxy_histories_helper': get_galaxy_histories,
            'bpatogalaxy_get_galaxy_libraries_helper': get_galaxy_libraries,
            'bpatogalaxy_get_s3_presigned_url_helper': get_s3_presigned_url
        }

