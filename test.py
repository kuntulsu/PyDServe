import subprocess
from importlib.util import find_spec as find_modules

r = find_modules("six")

try:
	print(r.submodule_search_locations[0])
except:
	print(r.origin)
