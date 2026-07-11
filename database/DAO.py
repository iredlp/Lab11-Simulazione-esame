from database.DB_connect import DBConnect
from model.arco import Arco
from model.artista import Artista


class DAO():

    @staticmethod
    def getAllGeneri():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Name 
                from genre g 
                order by g.Name  """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genere):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct a.*   
                    from artist a , genre g, track t , album a2 
                    where t.GenreId =g.GenreId and a2.ArtistId =a.ArtistId 
                    and t.AlbumId =a2.AlbumId and g.Name =%s
                    group by a.Name """

        cursor.execute(query, (genere, ))

        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges( genere, idMapArtisti):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t1.Artistid as a1, t2.Artistid as a2
                    from(
                    select a.ArtistId, i2.CustomerId
                    from album a , track t, invoiceline i, invoice i2, genre g
                    where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId 
                    and t.GenreId = g.GenreId and g.Name =%s
                    group by a.ArtistId, i2.CustomerId
                    ) as t1,
                    (select a.ArtistId, i2.CustomerId
                    from album a , track t, invoiceline i, invoice i2, genre g
                    where a.AlbumId = t.AlbumId and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId 
                    and t.GenreId = g.GenreId and g.Name =%s
                    group by a.ArtistId, i2.CustomerId) as t2
                    where t1.Customerid = t2.Customerid 
                    and t1.Artistid < t2.Artistid
                    group by t1.Artistid, t2.Artistid """

        cursor.execute(query, (genere, genere))

        #for row in cursor:
           # results.append(Arco(**row))
        for row in cursor:
            results.append(Arco(idMapArtisti[row["a1"]],idMapArtisti[row["a2"]],0))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getPop(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        artisti = {}
        query = """select a.ArtistId, sum(i.Quantity) as s
                    from album a, track t, invoiceline i, invoice i2, genre g
                    where a.AlbumId = t.AlbumId and i.TrackId = t.TrackId and t.GenreId = g.GenreId and g.Name = %s and i2.InvoiceId = i.InvoiceId 
                    group by a.ArtistId """
        cursor.execute(query, (genere,))

        for row in cursor:
            artisti[(row["ArtistId"])] = row["s"]
        cursor.close()
        cnx.close()
        return artisti

