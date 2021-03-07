--Question 1
SELECT MAX(Total)
FROM Invoice;

--Question 2
--Select shows the return value of max billing total
SELECT Invoice.Total
FROM Invoice
WHERE Invoice.Total > 24;

--Question 3
SELECT MediaType.Name, COUNT(*)
FROM Track, MediaType
--used the WHERE clause to join the tables
WHERE track.MediaTypeId = MediaType.MediaTypeId
GROUP BY MediaType.Name
ORDER BY MediaType.Name ASC;

--Question 4
SELECT MediaType.Name, COUNT(*)
FROM Track, MediaType
WHERE track.MediaTypeId = MediaType.MediaTypeId
GROUP BY MediaType.Name
ORDER BY COUNT(*) DESC;

--Question 5
SELECT MediaType.Name, COUNT(*) totalTrack
FROM Track, MediaType
WHERE track.MediaTypeId = MediaType.MediaTypeId
GROUP BY MediaType.Name
--HAVING is used with the GROUP BY to filter group result
HAVING COUNT(*) > 200;

--Question 6
SELECT COUNT(*), COUNT(DISTINCT Artist.Name)
FROM Track,Album,Artist
WHERE Track.AlbumId = Album.AlbumId AND Album.ArtistId = Artist.ArtistId AND Artist.Name LIKE 'A%';

--in class
--number of tracks, name beginning with 'A'
--artist, album, and track
SELECT count(*) total_track, count(DISTINCT art.Name) artist_count
FROM Artist art
join album al on art.ArtistId  = al.ArtistId
join Track tr on al.AlbumId = tr.AlbumId
WHERE art.Name like 'A%' OR art.Name like 'The A%';

--Question 7
SELECT FirstName || ' ' || LastName
FROM Employee;

--In class example
SELECT FirstName || ' ' || LastName employee_name, BirthDate,
       CASE WHEN BirthDate BETWEEN '1940-01-01' and '1958-01-01' THEN '40s'
            WHEN BirthDate BETWEEN '1950-01-01' and '1968-01-01' THEN '50s'
            WHEN BirthDate BETWEEN '1960-01-01' and '1978-01-01' THEN '60s'
        ELSE '70'
        END AS Decade
FROM Employee;


--In class example of a subquery
SELECT Country
FROM Customer
WHERE EXISTS
    (
        SELECT distinct Country
        FROM Customer
        WHERE PostalCode '78174'
        or Fax is not null
    );




