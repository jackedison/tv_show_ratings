import json  # Used to convert json api to python dict

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sbs  # Its a wrapper for matplotlib might as well install and make things look nicer

import call_api
import display


def read_in_jsons(json_path, tv_show):
    '''Read in tv_show data from local JSON db'''
    with open(json_path) as json_file:
        dic = json.load(json_file)
    return dic[tv_show]


def main(tv_show, refresh_data, display_data):
    '''Dictates where to pull data from and what to do with it'''
    if refresh_data:
        dic = call_api.get_api_data(tv_show=tv_show, start_season=1, 
                               start_episode=1, save_as_json=True)
    else:
        dic = read_in_jsons('tv_shows.json', tv_show)

    if display_data:
        fig, ax, plt = display.display_data(tv_show, dic)
        plt.show()


if __name__ == "__main__":
    ### ESSENTIAL INPUTS FOR PROGRAM HERE ###
    tv_show = 'House of Cards'
    tv_show = 'Friends'
    tv_show = 'Top Gear'
    tv_show = 'The Office'
    tv_show = 'Westworld'
    tv_show = 'Game of Thrones'

    # Request limit reached for today btw.

    display_data = True
    
    
    # Check if show in db and if not then fetch anyway
    refresh_data_master = False
    refresh_data = False
    tv_shows = call_api.TV_Shows()
    #tv_shows.remove_show(tv_show)

    if refresh_data_master or tv_show not in tv_shows.get_show_names():
        refresh_data = True

    main(tv_show, refresh_data, display_data)




