import json
import urllib.request
import pprint
import logging


def next_episode(season, episode, last_existed, print_new_line=True):
    ''' Returns next episode/season based on whether last one existed'''
    if last_existed == 'False':  # Boolean is stored as string in api
        if episode != 1:
            if print_new_line: print('')
            return season+1, 1
        else:
            return None, None
    return season, episode+1


# We could store in an sqlite3 db here but want to learn json + lightweight so using that
# If database got huge should migrate it to sqlite3 functionality
# Learned about .seek(0) method to go back to reading start of file with error here!
# If method breaks or wanna reset json just save it as {}

# Lets create a class to deal with our JSON object
class TV_Shows():
    def __init__(self):
        '''Create an empty dic for about 0 reason np'''
        self.dic = {}

    def read_json(self, json_dir='tv_shows.json'):
        '''Reads in json file and returns as python dic'''
        with open(json_dir, 'r') as master_file:
            self.dic = json.load(master_file)

    def add_file(self, tv_show, file):
        '''Add new file to current dic'''
        self.dic[tv_show] = file

    def save_json(self, json_dir='tv_shows.json', indent=4):
        '''Save current dic to json dir'''
        with open(json_dir, 'w') as master_file:
            json.dump(self.dic, master_file, indent=indent)

    def get_show_names(self):
        if self.dic == {}:
            self.read_json()
        names = sorted(list(self.dic.keys()))
        print('In current database: {}'.format(names))
        return names

    def remove_show(self, tv_show):
        self.read_json()
        if tv_show in self.dic:
            del(self.dic[tv_show])
        self.save_json()
        
    

if __name__ == "__main__":
    tv_shows = TV_Shows()
    tv_shows.get_show_names()



def get_api_data(tv_show, api_key='90b41255', start_season=1, start_episode=1, save_as_json=True):
    '''Gets OMBD api data for TV show and saves to a master JSON
       Note that the free api_key caps at 1000 calls a day'''
    logging.basicConfig(level=logging.INFO)

    # For url encoding space (ASCII 32) becomes 20 in hexa so replace with %20
    tv_show_url = tv_show.replace(' ', '%20')

    api_format = 'http://www.omdbapi.com/?t={}&Season={}&Episode={}&apikey={}'

    # Create a master dic to store json data pulled in
    master_file = []

    # Starting season and episode
    season, episode = start_season, start_episode

    # Fetch data. While next season exists, load into JSONS to use
    while season != None:
        api = api_format.format(tv_show_url, season, episode, api_key)
        # Open page and read in data using json library to a dict
        
        try:
            with urllib.request.urlopen(api) as api_page:
                data = json.load(api_page)
        except:
            raise TimeoutError('Likely daily request limit reached. Check failed API url manually here: {}'.format(api))

        # If got a response then store to master dic
        if data['Response'] == 'True':
            logging.info('Fetched data for Season {} - Episode {}, {}'.format(data['Season'], data['Episode'], data['Title']))
            master_file.append(data)

        # Check what next season/episode combo is based on last response
        season, episode = next_episode(season, episode, data['Response'])

    if save_as_json:
        tv_shows = TV_Shows()
        tv_shows.read_json()
        tv_shows.add_file(tv_show, master_file)
        tv_shows.save_json()

    return master_file