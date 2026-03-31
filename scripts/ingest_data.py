import pandas as pd
import duckdb
import os

DATA_DIR = 'data'
DB_PATH = 'database/ecommerce.duckdb'

def clean_and_ingest():

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = duckdb.connect(DB_PATH)

    files = {
        'customers': 'customers.csv',
        'products': 'products.csv',
        'events': 'events.csv',
        'transactions': 'transactions.csv',
        'campaigns': 'campaigns.csv'
    }

    for table_name, file_name in files.items():
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            print(f"can not find {file_name}.")
            continue

        df = pd.read_csv(file_path)

        # column name standardization
        df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]

        # String cleaning
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if '_id' in col:
                # id case
                df[col] = df[col].astype(str).str.strip().str.upper()
            else:
                # Title Case
                df[col] = df[col].astype(str).str.strip().str.title()

                df[col] = df[col].replace('Nan', 'Unknown').replace('None', 'Unknown')

        # timestamp transformation
        date_cols = [c for c in df.columns if 'date' in c or 'timestamp' in c]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        # ingest raw table
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
        print(f"Table [{table_name}] created. Added {len(string_cols)} columns")

    obt_view_sql = """
    CREATE OR REPLACE VIEW v_marketing_funnel AS 
    SELECT 
        e.*, 
        c.acquisition_channel,
        c.loyalty_tier,
        p.category AS product_category,
        p.base_price AS product_price,
        p.brand AS product_brand
    FROM events e
    LEFT JOIN customers c ON e.customer_id = c.customer_id
    LEFT JOIN products p ON e.product_id = p.product_id;
    """
    
    con.execute(obt_view_sql)

    con.close()
    print("\n All done.")

if __name__ == "__main__":
    clean_and_ingest()