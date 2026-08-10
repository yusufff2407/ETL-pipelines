import requests
import psycopg2
from datetime import datetime

# 1. EXTRACT
def extract_data():
    print("[EXTRACT] Fetching live crypto market prices...")
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd,eur"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("[EXTRACT] Successfully fetched data!")
        return response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

# 2. TRANSFORM
def transform_data(raw_data):
    print("[TRANSFORM] Cleaning and structuring records...")
    transformed_records = []
    fetch_time = datetime.now()

    for coin, prices in raw_data.items():
        usd_price = float(prices["usd"])
        eur_price = float(prices["eur"])
        eur_to_usd_rate = round(usd_price / eur_price, 4)

        transformed_records.append((
            coin.capitalize(),
            usd_price,
            eur_price,
            eur_to_usd_rate,
            fetch_time
        ))
    
    print(f"[TRANSFORM] Transformed {len(transformed_records)} records.")
    return transformed_records

# 3. LOAD
def load_data(records):
    print("[LOAD] Connecting to PostgreSQL...")
    
    conn = psycopg2.connect(
        dbname="crypto_de_db",
        user="postgres",
        password="YusufPOSTGRES", 
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS coin_market_prices (
            id SERIAL PRIMARY KEY,
            coin_name VARCHAR(50),
            price_usd NUMERIC(12, 2),
            price_eur NUMERIC(12, 2),
            eur_usd_rate NUMERIC(6, 4),
            fetched_at TIMESTAMP
        );
    """
    cur.execute(create_table_query)

    insert_query = """
        INSERT INTO coin_market_prices (coin_name, price_usd, price_eur, eur_usd_rate, fetched_at)
        VALUES (%s, %s, %s, %s, %s);
    """
    for record in records:
        cur.execute(insert_query, record)

    conn.commit()
    print(f"[LOAD] Successfully inserted {len(records)} records into Postgres!")

    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        raw_json = extract_data()
        clean_records = transform_data(raw_json)
        load_data(clean_records)
        print(" ETL PIPELINE COMPLETED SUCCESSFULLY!")
    except Exception as e:
        print(f"PIPELINE FAILED: {e}")