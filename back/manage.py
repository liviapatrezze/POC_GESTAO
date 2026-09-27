#!/usr/bin/env python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def main() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. O ambiente virtual está ativo?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
