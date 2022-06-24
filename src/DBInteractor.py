import pandas.io.sql as sqlio
import pandas as pd
from sqlalchemy import create_engine
import logging


class DBInteractor:
    """Class for interacting with the database"""

    def __init__(self, dbinfo):
        """An instance of the database interactor

        Args:
            dbinfo (dict): database information
        """
        self.dbinfo = dbinfo  # database info
        self.connection = None  # server connection
        logging.info("Initialized a DBInteractor instance")

    def connect_db(self):
        """Connect to the database"""

        # Establishing the connection
        logging.info("DBInteractor: Connecting to database...")

        try:

            # Create connection string
            postgres_str = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
                self.dbinfo["user"],
                self.dbinfo["password"],
                self.dbinfo["host"],
                self.dbinfo["port"],
                self.dbinfo["database"],
            )

            # Create connection engine
            self.connection = create_engine(postgres_str)
            # conn = psycopg2.connect(cnx)
            logging.info("DBInteractor: connection successful")

        except Exception as e:
            logging.exception("DBInteractor: Exception occured", exc_info=True)

    def pull_channel_promotion_data(self):
        """Pull channel and promotion processed data from the database

        Returns:
            pd.DataFrame: processed data with metrics information
        """

        # Ensure connection is present
        if self.connection is None:
            logging.exception(
                "DBInteractor: No connection exists. Please start a connection with self.connect_db().",
                exc_info=True,
            )
            return None

        # Run sql query
        try:
            logging.info("DBInteractor: Pulling data from database...")
            dat = pd.read_sql_query(
                con=self.connection,
                sql=""" 
                    SELECT
                        channel, 
                        promotion_type,
                        count(*) AS count_total,
                        count(CASE WHEN coupon_used THEN 1 END) AS coupon_true,
                        ROUND( 100.0 * count(CASE WHEN coupon_used THEN 1 END) / count(*), 2) AS percent_coupon_true,
                        count(CASE WHEN purchase THEN 1 END) AS purchase_true,
                        ROUND( 100.0 * count(CASE WHEN purchase THEN 1 END) / count(*), 2) AS percent_purchase_true
                    FROM
                        offers AS o
                    LEFT JOIN 
                        customers AS c ON o.user_id = c.user_id
                    WHERE 
                        TO_DATE( CONCAT(o.year,'-',o.week_number), 'YYYY-WW') > TO_DATE(c.signup_month, 'YYYY-DD')
                    GROUP BY 
                        o.channel, o.promotion_type;
                    """,
            )
            logging.info("DBInteractor: Successfully pulled data from database")

        except Exception as e:
            logging.exception("DBInteractor: Exception occured", exc_info=True)
            return None

        return dat

    def pull_timeseries_data(self):
        """Pull timeseries processed data from the database

        Returns:
            pd.DataFrame: processed data with metrics information
        """

        # Ensure connection is present
        if self.connection is None:
            logging.exception(
                "DBInteractor: No connection exists. Please start a connection with self.connect_db().",
                exc_info=True,
            )
            return None

        # Run sql query
        try:
            logging.info("DBInteractor: Pulling seasonal data from database...")
            dat = pd.read_sql_query(
                con=self.connection,
                sql=""" 
                    SELECT
                        o.year, 
                        o.week_number,
                        count(*) AS count_total,
                        count(CASE WHEN coupon_used THEN 1 END) AS coupon_true,
                        ROUND( 100.0 * count(CASE WHEN coupon_used THEN 1 END) / count(*), 2) AS percent_coupon_true,
                        count(CASE WHEN purchase THEN 1 END) AS purchase_true,
                        ROUND( 100.0 * count(CASE WHEN purchase THEN 1 END) / count(*), 2) AS percent_purchase_true
                    FROM
                        offers AS o
                    LEFT JOIN 
                        customers AS c ON o.user_id = c.user_id
                    WHERE 
                        TO_DATE( CONCAT(o.year,'-',o.week_number), 'YYYY-WW') > TO_DATE(c.signup_month, 'YYYY-DD')
                    GROUP BY 
                        o.year, o.week_number;
                    """,
            )
            logging.info(
                "DBInteractor: Successfully pulled seasonal data from database"
            )

        except Exception as e:
            logging.exception("DBInteractor: Exception occured", exc_info=True)
            return None

        return dat
