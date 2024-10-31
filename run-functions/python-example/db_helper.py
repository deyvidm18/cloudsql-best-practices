import logging
import os
import pymysql
import sqlalchemy
import faker
import flask

from google.cloud.sql.connector import Connector, IPTypes
from utils import access_secret_version

fake = faker.Faker()
logging.basicConfig(level=logging.INFO)  # Set the logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
logger = logging.getLogger(__name__)  # Create a logger instance
    
def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package and reads credentials from
    Secret Manager.
    """
    logger.info("Starting database connection...")
    # Access the secret payload
    secret_payload = access_secret_version(os.environ.get("SECRET_NAME"))

    # Parse the JSON payload
    import json
    secret_data = json.loads(secret_payload)

    instance_connection_name = secret_data["connection_name"]
    db_user = secret_data["db_user"]
    db_pass = secret_data["db_password"]
    db_name = secret_data["db_name"]

    logger.info("Secrets Done..")

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        """Connects to the database using either password or IAM auth."""
        if os.environ.get("DB_IAM_USER"):
            # Use IAM authentication
            conn: pymysql.connections.Connection = connector.connect(
                instance_connection_name,
                "pymysql",
                user=os.environ.get("DB_IAM_USER"),
                db=db_name,
                enable_iam_auth=True,
                ip_type=ip_type,
            )
        else:
            # Use password authentication
            conn: pymysql.connections.Connection = connector.connect(
                instance_connection_name,
                "pymysql",
                user=db_user,
                password=db_pass,
                db=db_name,
            )
        return conn
    logger.info("Connection Done..")
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # [START_EXCLUDE]
        # Pool size is the maximum number of permanent connections to keep.
        pool_size=int(os.environ.get("MAX_CONNECTIONS"),5),
        # Temporarily exceeds the set pool_size if no connections are available.
        max_overflow=0,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        pool_timeout=30,  # 30 seconds
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # re-established
        pool_recycle=1800,  # 30 minutes
        # [END_EXCLUDE]
    )
    return pool
# [END cloud_sql_mysql_sqlalchemy_connect_connector]

def insert_record(db: sqlalchemy.engine.base.Engine):
    """Saves a dummy record into the database.

    Args:
        db: Connection to the database.
    Returns:
        A HTTP response that can be sent to the client.
    """
    # [START cloud_sql_mysql_sqlalchemy_connection]
    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text(
        "INSERT INTO users (name, lastname) VALUES (:name, :lastname)"
    )
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, parameters={"name": fake.first_name(), "lastname": fake.last_name()})
            conn.commit()
    except sqlalchemy.exc.OperationalError as e:
        logger.exception("Operational error during insertion: %s", e)
    except sqlalchemy.exc.ProgrammingError as e:
        logger.exception("Programming error during insertion: %s", e)
    except Exception as e:
        logger.exception("An unexpected error occurred: %s", e)
        # [END_EXCLUDE]
    # [END cloud_sql_mysql_sqlalchemy_connection]
    logger.info("Inserted a row successfully in the database.")
    return flask.Response(
        status=200,
        response=f"Inserted a row successfully in the database.",
    )