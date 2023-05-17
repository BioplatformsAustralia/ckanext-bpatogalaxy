import logging

from ckan.plugins import toolkit as tk
from bioblend.galaxy import GalaxyInstance

log = logging.getLogger(__name__)


def get_galaxy_workflows():
    print("Initiating Galaxy connection")
    galaxy_host = tk.config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = tk.config.get('ckanext.bpatogalaxy.galaxy_api_key')

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
    galaxy_host = tk.config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = tk.config.get('ckanext.bpatogalaxy.galaxy_api_key')

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
    galaxy_host = tk.config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = tk.config.get('ckanext.bpatogalaxy.galaxy_api_key')

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
    bucket_path = tk.config.get('ckanext.s3filestore.aws_storage_path')
    bpa_resource_url = bucket_path + tk.config.get('ckanext.bpatogalaxy.galaxy_test_file')
    galaxy_host = tk.config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = tk.config.get('ckanext.bpatogalaxy.galaxy_api_key')
    token_key = tk.config.get('ckanext.bpatogalaxy.ckan_api_key')
    token_name= tk.config.get('ckanext.bpatogalaxy.ckan_api_key_name')
    
    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)

    histories = gi.histories.get_histories()

    url = bpa_resource_url

    if len(histories) >= 0:
        print("Uploading from history to url")
        gi.histories.upload_history_from_url(url=url,token_name=token_name,token_key=token_key)
    else:
        print("\nDo nothing!!!")

    return url
