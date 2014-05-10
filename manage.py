#!/usr/bin/env python
import sys

import finances


if __name__ == '__main__':
    if not sys.argv or 'help' in sys.argv:
        print('HELP text will be here!')

    elif 'run' in sys.argv:
        finances.app.run(host='localhost', port=8080, debug=True)

    else:
        print('Unknown command')
