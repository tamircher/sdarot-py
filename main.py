import argparse

from colorama import init, Fore, Style

from sdarot import SdarotPy
from searchSerie import search
from utils import center

init(autoreset=True)

MAX_EP_NUM = 50

if __name__ == "__main__":
    print("\n\n")
    print(Fore.GREEN + Style.BRIGHT + center(",d88~~\       888                             d8        888~-_           "))
    print(Fore.GREEN + Style.BRIGHT + center("8888     e88~\888   /~~~8e  888-~\  e88~-_  _d88__      888   \  Y88b  / "))
    print(Fore.GREEN + Style.BRIGHT + center("`Y88b   d888  888       88b 888    d888   i  888   ____ 888    |  Y888/  "))
    print(Fore.GREEN + Style.BRIGHT + center(" `Y88b, 8888  888  e88~-888 888    8888   |  888        888   /    Y8/   "))
    print(Fore.GREEN + Style.BRIGHT + center("   8888 Y888  888 C888  888 888    Y888   '  888        888_-~      Y    "))
    print(Fore.GREEN + Style.BRIGHT + center("\__88P'  \"88_/888  \"88_-888 888     \"88_-~   \"88_/      888        /     "))
    print(Fore.GREEN + Style.BRIGHT + center("                                                                 _/      "))
    print("\n")

    parser = argparse.ArgumentParser()

    parser.add_argument('--sid', type=int)
    parser.add_argument('-s', '--seasons', type=str, default='1')
    parser.add_argument('-e', '--episodes', type=str)
    parser.add_argument('--search', type=str)
    parser.add_argument('--out', type=str, default='output')

    args = parser.parse_args()

    if args.search:
        search(args.search)
    else:

        season_split = args.seasons.split('-')
        season_range = range(int(season_split[0]), int(season_split[-1]) + 1)

        episode_range = []
        if args.episodes is not None:

            episode_split = args.episodes.split('-')
            episode_range = range(
                int(episode_split[0]), int(episode_split[-1]) + 1)
        else:
            episode_range = range(1, MAX_EP_NUM)

        print(center(
            Fore.YELLOW +
            f'----====[ Fetching: Seasons {season_range[0]}-{season_range[-1]}, Episodes {episode_range[0]}-{episode_range[-1]} ]====----'))
        sdarot = SdarotPy(
            sid=args.sid,
            season_range=season_range,
            episode_range=episode_range,
            output_path=args.out,
        )

        sdarot.download_series()
