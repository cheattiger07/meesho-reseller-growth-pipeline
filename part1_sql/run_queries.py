import sqlite3, csv, os

con = sqlite3.connect("data/meesho_reseller.db")
names = ["monthly_category_revenue", "region_revenue", "top_resellers",
         "never_ordered", "count_star_vs_count_col", "june_delivered_aov"]
os.makedirs("part1_sql/output", exist_ok=True)

sql = open("part1_sql/queries.sql", encoding="utf-8").read()
chunks = [c.strip() for c in sql.split(";") if c.strip()]

for name, q in zip(names, chunks):
    cur = con.execute(q)
    with open(f"part1_sql/output/{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([d[0] for d in cur.description])
        w.writerows(cur.fetchall())
    print(name, "ok")