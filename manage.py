"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess
sys.path.insert(1,f"{os.getcwd()}/lib/python3.8/site-packages")
user = subprocess.Popen("whoami",stdout=subprocess.PIPE).communicate()[0].decode().replace("\n","")
if user != "root":
	print("please run the server as root")
	sys.exit()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PyDServe.settings')
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
