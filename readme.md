# Crypto ETL Pipeline

A simple Python ETL pipeline that fetches live cryptocurrency prices from the CoinGecko API, transforms the data, and stores it in PostgreSQL.

## How it works

The pipeline follows three basic steps:

**Extract**
- Fetches live Bitcoin, Ethereum, and Solana prices in USD and EUR from CoinGecko.

**Transform**
- Cleans the API response.
- Calculates the EUR → USD exchange rate.
- Adds a timestamp to each record.

**Load**
- Creates a PostgreSQL table if it doesn't exist.
- Inserts the transformed records into the database.

## Tech Stack

- Python
- Requests
- PostgreSQL
- psycopg2
- CoinGecko API

## Setup

Install the dependencies:

```bash
pip install requests psycopg2-binary
