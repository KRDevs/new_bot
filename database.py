import sqlite3 as sq

db = sq.connect('baza.db')
cursor = db.cursor()


async def db_start():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS User("
        "user_id TEXT PRIMARY KEY,"
        "username TEXT,"
        "firstname TEXT,"
        "lastname TEXT,"
        "created_at DATETIME,"
        "uz_balance,"
        "btc_balance,"
        "eth_balance,"
        "usdt_balance,"
        "bnb_balance,"
        "sol_balance,"
        "usdc_balance,"
        "xrp_balance,"
        "doge_balance,"
        "ton_balance,"
        "ada_balance,"
        "is_bot TEXT)"
    )
    db.commit()


async def create_user(user_id, username, firstname, lastname, created_at, is_bot, uz_balance, btc_balance, eth_balance,
                      usdt_balance, bnb_balance, sol_balance, usdc_balance, xrp_balance, doge_balance, ton_balance,
                      ada_balance):
    user = cursor.execute("SELECT 1 FROM User WHERE user_id=='{key}'".format(key=user_id)).fetchone()
    if not user:
        cursor.execute("INSERT INTO User VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (
                           user_id, username, firstname, lastname, created_at, is_bot, uz_balance, btc_balance,
                           eth_balance,
                           usdt_balance, bnb_balance, sol_balance, usdc_balance, xrp_balance, doge_balance, ton_balance,
                           ada_balance))
        db.commit()


async def get_user_balances(user_id):
    try:
        cursor.execute("SELECT uz_balance,btc_balance, eth_balance, usdt_balance,bnb_balance, "
                       "sol_balance,usdc_balance,xrp_balance,doge_balance,ton_balance, ada_balance"
                       "FROM User WHERE user_id=?", (user_id,))
        row = cursor.fetchone()

        if row:
            balances = {
                'BTC': row[0],
                'ETH': row[1],
                'USDT': row[2],
                'BNB': row[3],
                'SOL': row[4],
                'USDC': row[5],
                'XRP': row[6],
                'DOGE': row[7],
                'TON': row[8],
                'ADA': row[9],
                'UZS': row[10]
            }
            return balances
        else:
            return None

    except sq.Error as e:
        print(f"Error retrieving balances for user {user_id}: {e}")
        return None


async def update_balance(user_id, valute, new_balance):
    column_name = f"{valute.lower()}_balance"

    user = cursor.execute("SELECT 1 FROM User WHERE user_id=?", (user_id,)).fetchone()
    if user:
        cursor.execute(f"UPDATE User SET {column_name}=? WHERE user_id=?", (new_balance, user_id))
        db.commit()
        print(f"Updated {valute} balance for user {user_id} to {new_balance}")
    else:
        print(f"User with ID {user_id} not found")
