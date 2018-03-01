import logging

from access_control.models import DB as db

logger = logging.getLogger(__name__)


def db_exceptions(exception):
    logger.error(exception)
    db.session.rollback()
    return exception.__class__.__name__, 400, {"error": exception._message().replace("\n", " ")}
