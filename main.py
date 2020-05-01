import argparse
from sdarot import SdarotPy

MAX_EP_NUM = 50

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--sid', type=int, required=True)
    parser.add_argument('-s', '--seasons', type=str, required=True)
    parser.add_argument('-e', '--episodes', type=str)

    args = parser.parse_args()

    season_split = args.seasons.split('-')
    season_range = range(int(season_split[0]), int(season_split[-1]) + 1)

    episode_range = []
    if args.episodes is not None:

        episode_split = args.episodes.split('-')
        episode_range = range(
            int(episode_split[0]), int(episode_split[-1]) + 1)
    else:
        episode_range = range(1, MAX_EP_NUM)

    print(
        f'Fetching Seasons {season_range[0]}-{season_range[-1]}, Episodes {episode_range[0]}-{episode_range[-1]}')
    sdarot = SdarotPy(sid=args.sid, season_range=season_range,
                      episode_range=episode_range)

    sdarot.download_series()
