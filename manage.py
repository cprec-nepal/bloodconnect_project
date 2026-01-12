#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# pylint: disable=C0415
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodconnect_project.settings')
    try:
        execute_from_command_line(sys.argv)
    except Exception as exc:
        raise exc

if __name__ == '__main__':
    main()
