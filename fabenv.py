import os

setting_folder = 'fix'
version_file = os.path.join(setting_folder, '_version.py')

try:
    from fabconfig import *
except ImportError as exp:
    pass
