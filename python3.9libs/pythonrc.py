from __future__ import print_function
from __future__ import absolute_import

import inspect
import os

from searcher import searchersetup

# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved."
__status__ = "Release Candidate"

# current_file_path = os.path.abspath(
#     inspect.getsourcefile(lambda: 0)
# )


def main():
    searchersetup.main()


if __name__ == '__main__':
    main()
