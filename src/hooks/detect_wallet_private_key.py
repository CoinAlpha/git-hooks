import re
import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    private_key_files = []

    for filename in args.filenames:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if re.search("[0-9A-Fa-f]{64}", line) and not "noqa" in line for line in lines:
                private_key_files.append(filename)

    if private_key_files:
        for private_key_file in private_key_files:
            print(f'Private key found: {private_key_file}')
        return 1
    else:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())