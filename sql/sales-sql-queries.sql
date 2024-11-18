-- Monthly Sales Analysis
SELECT 
    DATE_TRUNC('month', order_date) as month, 
    product_category, 
    COUNT(DISTINCT order_id) as total_orders, 
    SUM(revenue) as total_revenue, 
    AVG(profit_margin) as avg_margin,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY 1, 2
ORDER BY 1 DESC, total_revenue DESC;

-- Customer Segmentation
WITH customer_sales AS (
    SELECT 
        customer_id, 
        SUM(revenue) as total_spend,
        COUNT(DISTINCT order_id) as order_count,
        AVG(profit_margin) as avg_margin
    FROM sales_data
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN total_spend > 5000 THEN 'High Value'
        WHEN total_spend BETWEEN 1000 AND 5000 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment,
    COUNT(*) as customer_count,
    AVG(total_spend) as avg_segment_spend
FROM customer_sales
GROUP BY 1
ORDER BY avg_segment_spend DESC;

-- Geographic Sales Analysis
SELECT 
    customer_country, 
    customer_city,
    SUM(revenue) as total_revenue,
    SUM(quantity) as total_units_sold,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY 1, 2
ORDER BY total_revenue DESC
LIMIT 10;

-- Product Performance
SELECT 
    product_category,
    product_name,
    SUM(quantity) as total_units_sold,
    SUM(revenue) as total_revenue,
    AVG(profit_margin) as avg_profit_margin
FROM sales_data
GROUP BY 1, 2
ORDER BY total_revenue DESC
LIMIT 10;
