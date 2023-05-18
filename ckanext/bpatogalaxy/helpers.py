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


def send_temp_presigned_url_to_galaxy(url):
    galaxy_host = tk.config.get('ckanext.bpatogalaxy.galaxy_host')
    galaxy_key = tk.config.get('ckanext.bpatogalaxy.galaxy_api_key')
    
    gi = GalaxyInstance(url=galaxy_host, key=galaxy_key)
    histories = gi.histories.get_histories()

    history_id = 0
    if len(histories) >= 0:
        for hist_dict in histories:
            history_id = hist_dict['id']
        if history_id > 0:
            tool_output = gi.tools.paste_content(url, history_id)
    else:
        history = histories.create_history(name="paste_url_BPA_to_Galaxy_history")
        history_id = history["id"]
        if history_id > 0:
            tool_output = gi.tools.paste_content(url, history_id)

    return url
