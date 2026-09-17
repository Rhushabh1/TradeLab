import logging
import sys
import structlog


# basic logger added early on in the project
# to avoid refactoring later
logging.basicConfig(format = "%(message)s",
					stream = sys.stdout,
					level = logging.INFO)

structlog.configure(wrapper_class = structlog.make_filtering_bound_logger(logging.INFO))

logger = structlog.get_logger()