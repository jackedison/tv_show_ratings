import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sbs  # Its a wrapper for matplotlib might as well install and make things look nicer

def display_data(tv_show, data):
    '''Takes in dic of data and displays tv ratings'''
    df = pd.DataFrame(data)
    # Convert rating to a float (all are strings read in as JSON uh)
    df['imdbRating'] = pd.to_numeric(df['imdbRating'], errors='coerce')

    # Used for plot positioning
    min_rating = min(df['imdbRating'])

    # Initial plt configs
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot each season in a loop so they are assigned unique colours
    running_episode = 0
    for i, season in enumerate(df['Season'].unique()):
        # Create temp_df for season and running episode tracker
        temp_df = df[df['Season'] == season].copy()
        temp_df['Running_Episode'] = pd.to_numeric(temp_df['Episode']) + running_episode

        # Plot main line
        ax.plot(temp_df['Running_Episode'], temp_df['imdbRating'], marker='o', color='C{}'.format(i))

        # Plot mean line
        mean = np.mean(temp_df['imdbRating'])
        xmin, xmax = min(temp_df['Running_Episode']), max(temp_df['Running_Episode'])
        ax.hlines(mean, xmin+0.3, xmax-0.3, color='C{}'.format(i), linestyle='--', alpha=0.35)
        ax.text(x=(xmax+xmin)/2, y=10.1, s='{:.1f}'.format(mean), ha='center', va='center')
        
        # Add vlines between the seasons (if not first run)
        if i > 0:
            x_at = min(temp_df['Running_Episode']) - 0.5
            ax.vlines(x_at, min_rating-0.3, 10, color='#666666', linewidth=0.5)

        # Add season text
        x_at = np.mean(temp_df['Running_Episode'])
        ax.text(x_at, min_rating-0.3, 'Season {}'.format(season), ha='center')

        running_episode += len(temp_df) # num to add to next ep number

        # Add episode name if top episode of season
        top_rated_eps = temp_df[temp_df['imdbRating'] == max(temp_df['imdbRating'])]
        for i, ep in top_rated_eps.iterrows():  # In case multiple top rated
            #ax.annotate(ep['Title'], (ep['Running_Episode'], ep['imdbRating']-0.05), rotation=90, va='top', ha='center')
            #ax.annotate(ep['imdbRating'], (ep['Running_Episode'], ep['imdbRating']+0.15), va='top', ha='center')
            pass

    # Fig/Ax customise outside of loop
    ax.yaxis.grid(color='#cccccc', linestyle='--')
    ax.set_xlim(0, len(df)+1)
    ax.tick_params(which='both', bottom=False, labelbottom=False)
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.set_yticks([i/10 for i in range(int(min_rating)*10, 101)], minor=True)
    # Ensure y-axis is integers
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

    ax.set_facecolor('#fffff9')

    ax.set_title('{} imdb Ratings'.format(tv_show), fontsize=24)
    ax.set_xlabel('Season', fontsize=22)
    ax.set_ylabel('imdb Rating', fontsize=22)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    

    plt.tight_layout()
    plt.savefig('{} imbd ratings.png'.format(tv_show))

    return fig, ax, plt



if __name__ == "__main__":
    import main
    tv_show = 'Breaking Bad'
    refresh_data = False
    display_data = True

    main.main(tv_show, refresh_data, display_data)






def display_data_og(tv_show, data):
    '''UNUSED - Original attempt using loop to plot all seasons as seperate graphs'''
    df = pd.DataFrame(data)

    # Convert rating to a float (all are strings read in as JSON uh)
    df['imdbRating'] = pd.to_numeric(df['imdbRating'], errors='coerce')
    df['imdbRating'][72] = 4.4

    # Initial plt configs
    total_seasons = len(df['Season'].unique())
    fig, axes = plt.subplots(1, total_seasons, sharey=True, figsize=(16, 8))
    fig.suptitle('{} imdb Ratings'.format(tv_show), fontsize=16)

    for i, season in enumerate(df['Season'].unique()):
        temp_df = df[df['Season'] == season]
        axes[i].plot(temp_df['Episode'], temp_df['imdbRating'], marker='o', color='C{}'.format(i))
        axes[i].set_frame_on(False)
        axes[i].set_xlabel('Season {}'.format(season))
        axes[i].tick_params(axis='both', which='both', left=False, bottom=False)

        if i > 0:
            frame1 = plt.gca()
            frame1.axes.get_yaxis().set_visible(False)

    plt.tight_layout()
    plt.savefig('{} imbd ratings.png'.format(tv_show))
    plt.show()