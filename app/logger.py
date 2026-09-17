import logging
import sys
import structlog


# basic logger added early on in the project
# to avoid refactoring later
logging.basicConfig(format = "%(message)s",
					stream = sys.stdout,
					level = logging.INFO)

# structlog.configure(wrapper_class = structlog.make_filtering_bound_logger(logging.INFO))
# now logs become JSON (nice format for each request)
structlog.configure(processors = [structlog.processors.TimeStamper(fmt = "iso"),
								structlog.processors.JSONRenderer()])

logger = structlog.get_logger()