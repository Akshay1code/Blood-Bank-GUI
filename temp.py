import csv
import backend.connection as db

stock_list = []

# IMPORTANT: utf-8-sig to remove BOM
with open("stock.csv", newline='', encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stock_list.append(row)

print(stock_list[:5])  # debug check first 5 rows

# DB insert
con = db.get_connection()
cursor = con.cursor()

query = """
INSERT INTO prbc_stock (blood_bank_id, blood_group, units_available)
VALUES (%s, %s, %s);
"""

for row in stock_list:
    try:
        cursor.execute(
            query,
            (
                int(row["blood_bank_id"]),
                row["blood_group"],
                int(row["units_available"])
            )
        )
    except Exception as e:
        print("Error inserting row:", row)
        print(e)

con.commit()
cursor.close()
con.close()

print("✅ PRBC stock imported successfully")
