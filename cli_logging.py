import argparse
import logging


class ViewCLI:
    @classmethod
    def get_args(cls):
        parser = argparse.ArgumentParser(
            description="sample description"
        )
        parser.add_argument(
            "-l",
            "--log",
            default="warning",
            help=("Provide logging level. " "Example --log debug', default='warning'"),
        )

        return parser.parse_args()


def handle_logging(args):
    levels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
    level = levels.get(args.log.lower())
    if level is None:
        raise ValueError(
            f"log level given: {args.log}"
            f" -- must be one of: {' | '.join(levels.keys())}"
        )
    if level is None:
        raise ValueError(
            f"log level given: {args.log}"
            f" -- must be one of: {' | '.join(levels.keys())}"
        )
    LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
    logging.basicConfig(level=level, format=LOG_FORMAT)


if __name__ == "__main__":
    args = ViewCLI.get_args()
    handle_logging(args)
    logging.info("starting...")
    logging.debug("Args are : %s", args)
