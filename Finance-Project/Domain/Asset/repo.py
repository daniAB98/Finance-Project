import sqlite3
from Domain.Asset.asset import Asset
from Domain.users.user import User

class AssetRepo:
    def add_to_user(self, user: User, asset: Asset):
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(f"main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"INSERT INTO '{table}' (ticker, name, country, units) "
                               f"VALUES ('{asset.ticker}', '{asset.name}', "
                               f"'{asset.country}', {asset.units})")
            except sqlite3.OperationalError:
                cursor.execute(f"CREATE TABLE '{table}' "
                               f"(ticker TEXT PRIMARY KEY, "
                               f"name TEXT, country TEXT, units REAL)")
                cursor.execute(f"INSERT INTO '{table}' (ticker, name, country, units) "
                               f"VALUES ('{asset.ticker}', '{asset.name}', "
                               f"'{asset.country}', {asset.units})")
            conn.commit()

    def get_for_user(self, user: User) -> list[Asset]:
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(f"main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM '{table}'")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return []
                else:
                    raise e
            assets_info = cursor.fetchall()
        assets = [Asset(
            ticker=x[0],
            nr=x[3],
            name=x[1],
            country=x[2],
            sector="sec"
        ) for x in assets_info]
        return assets