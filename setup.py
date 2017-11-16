"""
	When installing this project as a module, only the contents of skuvault module are included.
	Tested with Python 3.5.4

	Help With Setup.py: https://docs.python.org/3.5/distutils/sourcedist.html#manifest
"""
from setuptools import setup
import os


def get_all_sub_modules_for_path(path, recursive=True):
	"""Gets all modules inside of package, removes useless ones,
	and returns the directories only. All modules in these dirs
	will be included."""
	import glob
	all_modules = glob.glob(path, recursive=recursive)
	all_modules = [
		m_ for m_ in all_modules
		if len(m_.split(".")) == 1
		and "__init__" not in m_
		and "__pycache__" not in m_
	]

	return all_modules


# GET ALL MODULES
all_modules = [
	"skuvault",  # svexceptions and utils
]
paths_to_traverse = [
	"skuvault\\sv_adapter\\**".replace("\\", os.sep),
]
for p_ in paths_to_traverse:
	all_modules.extend(get_all_sub_modules_for_path(p_))


setup(
	# name of installation
	name="skuvault",

	# version number (try getting out of a project file instead!)
	version="1.0.1",

	# modules to include
	packages=all_modules,

	# first param is where to save the files; 2nd is list of files to save there
	data_files=[],

	# any modules available on pypi
	install_requires=[],

	# ?
	# package_dir={"": "skuvault"},  # https://docs.python.org/3.5/distutils/setupscript.html
)
