import flask
import functions_framework
import logging 

from db_helper import connect_with_connector, insert_record

db = None

logger = logging.getLogger(__name__)  # Create a logger instance

@functions_framework.http
def main(request: flask.Request) -> flask.Response:
    global db
    # initialize db within request context
    if not db:
        # initiate a connection pool to a Cloud SQL database
        db = connect_with_connector()
    return insert_record(db)

