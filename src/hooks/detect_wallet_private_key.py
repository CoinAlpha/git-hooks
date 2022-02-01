import re
import argparse
from typing import Optional
from typing import Sequence

WHITELIST = ['mock', 'documentation']

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    private_key_files = []

    for filename in args.filenames:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if re.search("[0-9A-Fa-f]{64}", line):
                    for allowed in WHITELIST:
                        if not f"noqa: {allowed}" in line:
                            private_key_files.append(filename)
                            break

    if private_key_files:
        for private_key_file in private_key_files:
            print(f'{private_key_file} contains line(s) that include same pattern as a wallet private key.')
        print('Either remove those lines or add a "noqa: {REASON}" tag comment on such lines.')
        print(f'REASON can be on of the following: {WHITELIST}.')
        return 1
    else:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())