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
        print("There are Histories found "+len(histories))

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


def send_temp_presigned_url_to_galaxy(resource_id):
    galaxy_host = tk.config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = tk.config.get('ckanext.bpatogalaxy.galaxy_api_key')
    galaxy_drs_proxy = tk.config.get('ckanext.bpatogalaxy.galaxy_drs_proxy')
    error = False
    user = tk.g.userobj
    if not user:
        error = True
        return error
    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)
    bpa_user = gi.users.get_users(f_email=user.email)
    if len(bpa_user) == 0:
        error = True
        return error
    bpa_user = bpa_user[0]
    url = f"drs://{galaxy_drs_proxy}/{resource_id}"
    gi.json_headers["run_as"] = bpa_user["id"]
    result = gi.histories.upload_dataset_from_library(url=url)
    if not result:
        error = True
        return error
    return error
