from argparse import ArgumentParser

from file_sorter import FileSorter


def define_args() -> ArgumentParser:
    parser = ArgumentParser(description='Sort files in directories named from creation or modification date')
    parser.add_argument('-s', '--source', help='Source directory', required=True)
    parser.add_argument('-d', '--destination', help='Destination directory', required=True)
    parser.add_argument('-c', '--creation', help='Sort by creation', action='store_true', default=True)
    parser.add_argument('-m', '--modification', help='Sort by modification', action='store_true')

    return parser.parse_args()


def main():
    args = define_args()
    sorter = FileSorter(args.source, args.destination, args.creation, args.modification)

    sorter.sort()


if __name__ == '__main__':
    main()
