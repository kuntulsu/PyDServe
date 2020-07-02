from importlib.util import find_spec as find_mod
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
def module_required(modules):
	def mod_check(request,*args,**kwargs):
		if modules is not None:
			if isinstance(modules,str):
				if find_mod(modules) is not None:
					return True
				else:
					return False
			elif isinstance(modules,list):
				
				for x in modules:
					if find_mod(x) is not None:
						pass
					else:
						return False
						break
				return True
			else:
				raise ValueError(f"Expecting str or list {type(modules)} was given")

	return user_passes_test(mod_check,login_url="../modules?mod_error=true")

def ajax_required(view):
	@wraps(view)
	def _wrapped_view(request, *args, **kwargs):
		if request.is_ajax():
			return view(request, *args, **kwargs)
		else:
			raise PermissionDenied()
	return _wrapped_view