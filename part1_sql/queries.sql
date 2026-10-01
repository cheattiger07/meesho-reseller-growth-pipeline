--Query 1: Monthly revenue by category
select month, category, ROUND(SUM(quantity * unit_price),2) as revenue,count(*) as n_orders
from orders
group by month, category
order by month, category;
--Query 2: Region-wise revenue and order count
select region, Round(sum(quantity * unit_price),2) as revenue, count(*) as n_orders
from orders o 
join resellers r on o.reseller_id = r.reseller_id
group by r.region
order by revenue desc;
--Query 3: top resellers by total spend
select r.reseller_id, r.reseller_name, ROUND(SUM(o.quantity * o.unit_price),2) as total_spend
from orders o
join resellers r on o.reseller_id = r.reseller_id
group by r.reseller_id, r.reseller_name
having sum(o.quantity * o.unit_price) > 50000
order by total_spend desc
limit 5;
--Query 4:Reseller who have never placed an order
select r.reseller_id,r.reseller_name 
from resellers r 
left join orders o 
on r.reseller_id = o.reseller_id
where o.order_id is null;
select r.reseller_id,
count(*) as count_star,
count(o.order_id) as count_order_id
from resellers r
left join orders o on r.reseller_id = o.reseller_id
where r.reseller_id = 'RS024'
GROUP by r.reseller_id;
--Query 5: Average order value for june,delivered orders only
select Round(sum(quantity * unit_price)/count(*),2) as aov
from orders
where month = 'June' and status = 'Delivered';

