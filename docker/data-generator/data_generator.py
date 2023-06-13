"""Data generator."""
from time import sleep

import pandas as pd
import psycopg2
from psycopg2.extensions import connection
from sklearn.datasets import load_iris


def create_table(pg_client: connection) -> None:
    """Create a table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS iris_data (
        id SERIAL PRIMARY KEY,
        timestamp text,
        sepal_length float8,
        sepal_width float8,
        petal_length float8,
        petal_width float8,
        target int
    );"""
    print(create_table_query)
    with pg_client.cursor() as cur:
        cur.execute(create_table_query)
        pg_client.commit()


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


def main(pg_client: connection) -> None:
    """Run main function."""
    # Create a table
    create_table(pg_client=pg_client)

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
                TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS'),
                {data.sepal_length},
                {data.sepal_width},
                {data.petal_length},
                {data.petal_width},
                {data.target}
            );
        """
        print(f"\nCount: {cnt}\n" f"Query: {insert_row_query}\n")

        with pg_client.cursor() as cur:
            cur.execute(insert_row_query)
            pg_client.commit()

        cnt += 1
        sleep(2)


if __name__ == "__main__":
    pg_client = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="postgres",
        port=5432,
        database="postgres",
    )

    main(pg_client=pg_client)
