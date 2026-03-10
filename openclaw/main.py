"""OpenClaw entry point."""

from openclaw.bot.application import build_application
from openclaw.utils.logging import configure_logging


def main() -> None:
    configure_logging()
    app = build_application()
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
