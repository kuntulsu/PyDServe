#!/usr/bin/python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
sys.path.insert(1,"lib/python3.8/site-packages")
print("Validating the User...")
if os.geteuid() != 0:
	print("please run the script as super user\nExiting...")
	sys.exit()
print("Access Granted, Continue to runserver procedure..")
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kraity.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
