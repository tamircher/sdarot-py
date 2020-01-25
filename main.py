import argparse
from sdarot import SdarotPy

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--sid', type=int, required=True)
    parser.add_argument('-s', '--seasons', type=str, required=True)
    parser.add_argument('-e', '--episodes', type=str, required=True)

    args = parser.parse_args()

    season_split = args.seasons.split('-')
    season_range = range(int(season_split[0]), int(season_split[-1]) + 1)

    episode_split = args.episodes.split('-')
    episode_range = range(
        int(episode_split[0]), int(episode_split[-1]) + 1)

    print(
        f'Fetching Seasons {season_range[0]}-{season_range[-1]}, Episodes {episode_range[0]}-{episode_range[-1]}')
    sdarot = SdarotPy(sid=args.sid, season_range=season_range,
                      episode_range=episode_range)

    sdarot.download_series()
