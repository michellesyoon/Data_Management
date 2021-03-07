/*1) Create a table Player with the following attributes.
     You will also define what the data types are going to be.
     a.pID(not null, primary key)
     b. name (not null)
     c. teamName
*/
CREATE TABLE Player (
    pID int not null ,
    name varchar(20) not null ,
    teamName varchar(20),
    primary key (pID)

);

--2)Alter the Player table to add a new column, age
ALTER TABLE Player
ADD age int;

/*3)Insert the following tuples(rows) into the Player table
    a. (1,'Player 1', 'Team A', 23)
    b. (2,'Player 2', 'Team A')
    c. (3,'Player 3', 'Team B', 28)
    d. (4,'Player 4', 'Team B')
 */
INSERT INTO Player
VALUES (1,'Player 1', 'Team A', 23),
       (2,'Player 2', 'Team A', NULL),
       (3,'Player 3', 'Team B', 28),
       (4,'Player 4', 'Team B', NULL);

--4)Update the Player table to delete Player 2's record from it
DELETE FROM Player
WHERE name = 'Player 2';

--5)Update the Player table to set age = 25 for tuples where age attribute is NULL
UPDATE Player
SET age = 25
WHERE age IS NULL ;

/*6)Write a query to return the number of tuples(row) and average age from
    the Player table
 */
SELECT COUNT(*) total_tuple, AVG(age) average_age
FROM Player;

--7)Drop the Player table
DROP TABLE Player;

/*8)Write a	query to return	the	average	Total of invoices where	the
    billing	country	is	Brazil.
 */
SELECT AVG(Total) total_invoice
FROM Invoice
WHERE BillingCountry in ('Brazil');

/*9)Write a	query to return	the	average	Total per billing city of invoices where
    the	billing	country	is Brazil.
 */
SELECT BillingCity, AVG(Total)
FROM Invoice
WHERE BillingCountry in ('Brazil')
GROUP BY BillingCity
ORDER BY BillingCity ASC;

--Trouble
--10)Write a query to return the names of all albums which have a more than 20 tracks
SELECT Album.Title, COUNT(TrackId) tracks
FROM Album, Track
WHERE Album.AlbumId = Track.AlbumId
GROUP BY Album.Title
HAVING tracks > 20
ORDER BY Album.Title ASC;

--Trouble
--11)Write a query to show how many	invoices were processed	in the year	2010.
SELECT COUNT(InvoiceDate) InvoiceProcessIn2010
FROM Invoice
WHERE InvoiceDate LIKE '2010%'
ORDER BY InvoiceDate ASC;

--12)Write a query to answer how many distinct billing cities there	are	per	each billing country.
SELECT BillingCountry, COUNT(DISTINCT BillingCity)
FROM Invoice
GROUP BY BillingCountry
ORDER BY BillingCountry ASC;

--13)Write a query to show the album title,	track name, and	media type name	for	each record.
SELECT Album.Title, Track.Name, MediaType.Name
FROM Album, Track, MediaType
WHERE Track.MediaTypeId = MediaType.MediaTypeId AND Album.AlbumId = Track.AlbumId
GROUP BY Album.Title
ORDER BY Album.Title ASC;

--Trouble
/*14)Write a query to find how many sales (invoice count) did Jane Peacock make as a support representative.
     In the	Customers table, you will find that	SupportRepId maps to an employeeID in the Employees	table that
     you can use. I	recommend using	a subquery for this.
 */
SELECT COUNT(Invoice.InvoiceId)
FROM Invoice, Customer
WHERE Invoice.InvoiceId = Customer.CustomerId
AND Customer.SupportRepId =
    (
        SELECT EmployeeId
        FROM Employee
        WHERE Employee.FirstName = 'Jane' AND Employee.LastName = 'Peacock'
    );












