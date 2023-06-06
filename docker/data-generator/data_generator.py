"""Data generator."""
from time import sleep

import pandas as pd
import psycopg2
from psycopg2.extensions import connection
from sklearn.datasets import load_iris


def create_table(db_connect: connection) -> None:
    """Create a table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS iris_data (
        id SERIAL PRIMARY KEY,
        timestamp timestamp,
        sepal_length float8,
        sepal_width float8,
        petal_length float8,
        petal_width float8,
        target int
    );"""
    print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()


def load_data() -> pd.DataFrame:
    """Load data."""
    inputs, labels = load_iris(return_X_y=True, as_frame=True)
    df = pd.concat([inputs, labels], axis="columns")
    rename_rule = {
        "sepal length (cm)": "sepal_length",
        "sepal width (cm)": "sepal_width",
        "petal length (cm)": "petal_length",
        "petal width (cm)": "petal_width",
    }
    df = df.rename(columns=rename_rule)
    return df


def main(db_connect: connection) -> None:
    """Run main function."""
    # Create a table
    create_table(db_connect=db_connect)

    # Load iris data
    df = load_data()

    # Generate data continuously
    cnt = 0
    while True:
        data = df.sample(1).squeeze()

        insert_row_query = f"""
        INSERT INTO iris_data
            (timestamp, sepal_length, sepal_width, petal_length, petal_width, target)
            VALUES (
                NOW(),
                {data.sepal_length},
                {data.sepal_width},
                {data.petal_length},
                {data.petal_width},
                {data.target}
            );
        """
        print(f"\nCount: {cnt}\n" f"Query: {insert_row_query}\n")
        with db_connect.cursor() as cur:
            cur.execute(insert_row_query)
            db_connect.commit()

        cnt += 1
        sleep(5)


if __name__ == "__main__":
    db_connect = psycopg2.connect(
        user="source",
        password="source",
        host="source-db",
        port=5432,
        database="source",
    )
    main(db_connect=db_connect)
