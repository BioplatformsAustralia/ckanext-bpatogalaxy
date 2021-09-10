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
        print("There are Histories found "+len(histories))

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
    host_name = config.get('ckanext.s3filestore.host_name')
    bucket_name = config.get('ckanext.s3filestore.aws_bucket_name')
    region = config.get('ckanext.s3filestore.region_name')
    p_key = config.get('ckanext.s3filestore.aws_access_key_id')
    s_key = config.get('ckanext.s3filestore.aws_secret_access_key')
    bucket_path = config.get('ckanext.s3filestore.aws_storage_path')
    bucket_path_key = bucket_path +  config.get('ckanext.bpatogalaxy.galaxy_test_file')
    galaxy_host = config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = config.get('ckanext.bpatogalaxy.galaxy_api_key')
    
    print(" ================================ ")
    print(" ================================ host_name "+host_name)
    print(" ================================ ")
    print(" ================================ bucket_name "+bucket_name)
    print(" ================================ ")
    print(" ================================ region "+region)
    print(" ================================ ")
    print(" ================================ p_key "+p_key)
    print(" ================================ ")
    print(" ================================ bucket_path_key "+bucket_path_key)

    s3 = boto3.session.Session(aws_access_key_id=p_key,
                               aws_secret_access_key=s_key,
                               region_name=region)

    client = s3.client(service_name='s3', endpoint_url=host_name)

    url = client.generate_presigned_url(ClientMethod='get_object',
                                        Params={'Bucket': bucket_name,
                                                'Key': bucket_path_key},
                                        ExpiresIn=300)
    
    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)

    histories = gi.histories.get_histories()

    print(" ================================ ")
    print(" ================================ url "+url)
    history_id = 0
    if len(histories) >= 0:
        print(" ================================ ")
        print(" ================================ Uploading to existing history from url")
        for hist_dict in histories:
            print(" ================================ iterate")
            # hist_details = histories.show_history(hist_dict['id'])
            # print("{} ({}) : {}".format(hist_dict['name'], hist_details['size'], hist_dict['id']))
            print(" ================================ hist_dict['id'] "+str(hist_dict['id']))
            history_id = hist_dict['id']
        if history_id > 0:
            print(" ================================ ")
            print(" ================================ existing history_id "+str(history_id))
            tool_output = gi.tools.paste_content(url, history_id)
            print(" ================================ ")
            print(" ================================ tool_output "+str(tool_output))
    else:
        print(" ================================ ")
        print(" ================================ Uploading to newly created history from url")
        history = histories.create_history(name="paste_url_BPA_to_Galaxy_history")
        history_id = history["id"]
        if history_id > 0:
            print(" ================================ ")
            print(" ================================ created history_id "+str(history_id))
            tool_output = gi.tools.paste_content(url, history_id)
            print(" ================================ ")
            print(" ================================ tool_output "+str(tool_output))

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

