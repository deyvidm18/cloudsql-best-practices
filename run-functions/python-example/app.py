from flask import Flask, request, Response
from faker import Faker
import sqlalchemy
from db_helper import connect_with_connector, insert_record
import logging

app = Flask(__name__)
logger = logging.getLogger()
db = connect_with_connector() 


@app.route('/', methods=['POST','GET'])  # Use POST for Cloud Run
def main():
    global db
    # initialize db within request context
    if not db:
        # initiate a connection pool to a Cloud SQL database
        db = connect_with_connector()
    return insert_record(db)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))