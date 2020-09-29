import argparse
from colorama import init, Fore, Style
from sdarot import SdarotPy
from searchSeries import search
from guidedSearchSeries import guided_search
from utils import center
from configuration import Configuration
import sys

init(autoreset=True)

MAX_SEASONS_NUM = 20
MAX_EPISODES_NUM = 50

if __name__ == "__main__":
    print("\n\n", end='')
    print(
        Fore.GREEN + Style.BRIGHT + center(",d88~~\       888                             d8        888~-_           "),
        end='')
    print(
        Fore.GREEN + Style.BRIGHT + center("8888     e88~\888   /~~~8e  888-~\  e88~-_  _d88__      888   \  Y88b  / "),
        end='')
    print(
        Fore.GREEN + Style.BRIGHT + center("`Y88b   d888  888       88b 888    d888   i  888   ____ 888    |  Y888/  "),
        end='')
    print(
        Fore.GREEN + Style.BRIGHT + center(" `Y88b, 8888  888  e88~-888 888    8888   |  888        888   /    Y8/   "),
        end='')
    print(
        Fore.GREEN + Style.BRIGHT + center("   8888 Y888  888 C888  888 888    Y888   '  888        888_-~      Y    "),
        end='')
    print(Fore.GREEN + Style.BRIGHT + center(
        "\__88P'  \"88_/888  \"88_-888 888     \"88_-~   \"88_/      888        /     "),
        end='')
    print(
        Fore.GREEN + Style.BRIGHT + center("                                                                 _/      "),
        end='')
    print("\n", end='')

    parser = argparse.ArgumentParser()

    parser.add_argument('--sid', type=int, help='series id')
    parser.add_argument('-s', '--seasons', type=str, help='the season number. example -s=1 -s=1-3')
    parser.add_argument('-e', '--episodes', type=str, help='the season number. episodes -s=1 -s=1-3')
    parser.add_argument('--search', type=str)
    parser.add_argument('-gs', '--guidedSearch', type=str, help='search and download multiple series')
    parser.add_argument('-out', '--output', type=str, default=f'{Configuration.OUTPUT_PATH}',
                        help='override the default output path.')

    args = parser.parse_args()
    if args.guidedSearch:
        selection = guided_search(args.guidedSearch)
        for index, element in enumerate(selection):
            if int(element[0]['code']) == -1:
                print('You selected to exit without downloading Series')
                print('Download aborted')
                sys.exit(1)

        for index, element in enumerate(selection):
            args.sid = int(element[0]['code'])
            season_range = range(1, MAX_SEASONS_NUM)
            episode_range = range(1, MAX_EPISODES_NUM)

            print(center(
                Fore.YELLOW +
                f'----====[ Fetching: Seasons {season_range[0]}-{season_range[-1]}, Episodes {episode_range[0]}-{episode_range[-1]} ]====----'))
            sdarot = SdarotPy(
                sid=args.sid,
                # season_range=season_range,
                # episode_range=episode_range,
                output_path=args.output,
            )

            sdarot.download_series()
        sys.exit(0)

    if args.search:
        search(args.search)
    else:

        if args.sid is None:
            print(Fore.RED + 'Missing --sid parameter\n')
            parser.print_help(sys.stderr)
            sys.exit(1)

        season_range = None
        if args.seasons is not None:

            season_split = args.seasons.split('-')
            season_range = range(int(season_split[0]), int(season_split[-1]) + 1)

        episode_range = range(1, MAX_EPISODES_NUM)
        if args.episodes is not None:

            episode_split = args.episodes.split('-')
            episode_range = range(
                int(episode_split[0]), int(episode_split[-1]) + 1)

        sdarot = SdarotPy(
            sid=args.sid,
            season_range=season_range,
            episode_range=episode_range,
            output_path=args.output,
        )

        sdarot.download_series()
