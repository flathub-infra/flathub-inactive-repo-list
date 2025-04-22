import logging
import re
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()


def validate(path: str):
    regex = "^[A-Za-z_][\\w\\-]*$"

    with open(path) as file:
        for line in file:
            appid = line.strip()
            split = appid.split(".")
            if (
                len(appid) > 255
                or len(split) < 3
                or not all(re.match(regex, sp) for sp in split)
            ):
                logger.error("Error: %s", appid)
                sys.exit(1)

    logger.info("All IDs are valid")


if __name__ == "__main__":
    validate("inactive.txt")
