--Question 1
SELECT FirstName, LastName, Email
FROM Employee;

--Question 2
SELECT *
FROM Artist;

--Question 3
SELECT *
FROM Employee
--%Manage: Finds any string that end with Manage
WHERE Title LIKE '%Manager';

--Question 4
SELECT MAX(Total), MIN(Total)
FROM Invoice;

--Question 5
SELECT BillingAddress, BillingCity, BillingPostalCode, total
FROM Invoice
WHERE BillingCountry IN ('Germany');

--Question 6
SELECT BillingAddress, BillingCity, BillingPostalCode, Total
FROM Invoice
WHERE Total >= 15 AND Total <= 25;

--Question 7
SELECT DISTINCT BillingCountry
FROM Invoice;

--Question 8
SELECT FirstName, LastName, CustomerId, Country
FROM Customer
WHERE Country NOT IN ('USA');

--Question 9
SELECT FirstName, LastName, CustomerId, Country
FROM Customer
WHERE Country IN ('Brazil');

--Question 10
SELECT *
FROM Track
ORDER BY Name;


