


import sqlite3
import pandas as pd


conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)


df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName, e.jobTitle
    FROM employees e
    JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)


df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING COUNT(e.employeeNumber) = 0
""", conn)


df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)


df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone,
           c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o
        ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName
""", conn)


df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName,
           p.amount, p.paymentDate
    FROM customers c
    JOIN payments p
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)


df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName,
           COUNT(c.customerNumber) AS n_customers
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY n_customers DESC
""", conn)


df_product_sold = pd.read_sql("""
    SELECT p.productName,
           COUNT(od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC
""", conn)


df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC
""", conn)


df_customers = pd.read_sql("""
    SELECT COUNT(c.customerNumber) AS n_customers,
           o.officeCode, o.city
    FROM offices o
    JOIN employees e
        ON o.officeCode = e.officeCode
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
""", conn)

20 
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,
           ofc.city, ofc.officeCode
    FROM employees e
    JOIN offices ofc
        ON e.officeCode = ofc.officeCode
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders o
        ON c.customerNumber = o.customerNumber
    JOIN orderdetails od
        ON o.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails od2
        JOIN orders o2
            ON od2.orderNumber = o2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT o2.customerNumber) < 20
    )
""", conn)


print(len(df_boston), len(df_zero_emp), len(df_employee))
print(len(df_contacts))   # should be 24
print(len(df_credit))     # should be 4
print(df_payment.head())
print(df_under_20.head())
# ---------------------------------------------------------------

conn.close()