import sqlite3
import pandas as pd

# Create in-memory database
conn = sqlite3.connect(":memory:")

# Created sample business dataset
data = pd.DataFrame({
    "customer_id": range(1, 101),
    "region": ["North", "South", "East", "West"] * 25,
    "purchase_amount": [round(x, 2) for x in (100 + 50 * pd.Series(range(100)).apply(lambda x: x % 10))],
    "product_category": ["A", "B", "C", "D"] * 25
})

# Loaded into SQL
data.to_sql("sales", conn, index=False, if_exists="replace")

# --- SQL QUERIES ---

print("Total Revenue:")
query1 = "SELECT SUM(purchase_amount) AS total_revenue FROM sales"
print(pd.read_sql(query1, conn))


print("\nRevenue by Region:")
query2 = """
SELECT region, SUM(purchase_amount) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC
"""
print(pd.read_sql(query2, conn))


print("\nAverage Purchase by Category:")
query3 = """
SELECT product_category, AVG(purchase_amount) AS avg_purchase
FROM sales
GROUP BY product_category
"""
print(pd.read_sql(query3, conn))


print("\nTop 5 Customers by Spend:")
query4 = """
SELECT customer_id, purchase_amount
FROM sales
ORDER BY purchase_amount DESC
LIMIT 5
"""
print(pd.read_sql(query4, conn))

import matplotlib.pyplot as plt

# Visualization: Revenue by Region
df_region = pd.read_sql(query2, conn)

df_region.plot(kind="bar", x="region", y="revenue")
plt.title("Revenue by Region")
plt.ylabel("Revenue")
plt.show()


# Visualization: Avg Purchase by Category
df_category = pd.read_sql(query3, conn)

df_category.plot(kind="bar", x="product_category", y="avg_purchase")
plt.title("Average Purchase by Category")
plt.ylabel("Avg Purchase")
plt.show()
