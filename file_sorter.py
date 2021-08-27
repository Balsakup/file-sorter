from datetime import datetime
from enum import Enum
from os.path import basename
from pathlib import Path
from shutil import copy

from tqdm import tqdm


class SortType(Enum):
    CREATION = 'creation'
    MODIFICATION = 'modification'


class FileSorter:
    def __init__(self, source: str, destination: str, sort_by_creation: bool, sort_by_modification: bool):
        self._source = Path(source)
        self._destination = Path(destination)
        self._sort_by_creation = sort_by_creation
        self._sort_by_modification = sort_by_modification
        self._ignored_files = ['.DS_Store']

    def sort(self):
        self._prepare_directories()

        progress = tqdm(total=len([filename for filename in self._source.iterdir()]))

        for filename in self._source.iterdir():
            progress.update()

            file = Path(filename)

            if file.is_dir() or basename(filename) in self._ignored_files:
                continue

            time_field = file.stat().st_mtime if self._sort_type() == SortType.MODIFICATION else file.stat().st_ctime
            time = datetime.fromtimestamp(time_field)
            destination_dir = self._destination.joinpath(time.strftime('%Y%m%d'))

            if not destination_dir.is_dir():
                destination_dir.mkdir(parents=True)

            copy(file, destination_dir.joinpath(basename(file)))

        progress.close()

    def _sort_type(self) -> SortType:
        return SortType.MODIFICATION if self._sort_by_modification else SortType.CREATION

    def _prepare_directories(self):
        if not self._source.is_dir():
            raise f'{self._source} is not a directory'

        if not self._destination.is_dir():
            self._destination.mkdir(parents=True)
