# Part 1 — SQL Outputs

This folder has the CSV files generated from the SQL queries in Part 1 of the Meesho analytics pipeline.

## Files

| File                           | Description                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------- |
|  monthly_category_revenue.csv  | Monthly revenue and order count by category. Used later in Part 2 and Part 4. |
|  region_revenue.csv            | Revenue and order count by region.                                            |
|  top_resellers.csv             | Top 5 resellers with total spending above 50,000.                             |
|  never_ordered.csv             | Resellers who have no orders.                                                 |
|  count_star_vs_count_col.csv   | Comparison of  COUNT(*)  and  COUNT(order_id) for RS024.                     |
|  june_delivered_aov.csv        | Average Order Value for Delivered orders in June.                             |

##  COUNT(*)  vs  COUNT(order_id)

I ran into a small issue while checking resellers who had no orders.

With a LEFT JOIN, a reseller is still kept in the result even when there is no matching order. In that case, the order columns are `NULL`.

For example, RS024 has no orders:

| reseller_id | reseller_name | count_star | count_order_id |
| ----------- | ------------- | ---------: | -------------: |
| RS024       | (name)        |        1   |            0   |

COUNT(*) returns  1 because the LEFT JOIN still produces a row for RS024.

COUNT(order_id) returns 0 because order_id is NULL in that row.

So using COUNT(*) = 0 to find resellers with no orders would give the wrong result.

I used:

sql
COUNT(o.order_id)


or, when filtering for unmatched rows:

sql
WHERE o.order_id IS NULL


The count_star_vs_count_col.csv file is included to show this difference clearly.
