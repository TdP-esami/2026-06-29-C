from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct art.ArtistId, art.Name
                from artist art, album al, track t
                where art.ArtistId = al.ArtistId
                and al.AlbumId = t.AlbumId
                order by art.Name
                """

        cursor.execute(query)

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()

        for artist in results:
            artist.Tracks = DAO.getTracksForArtist(artist.ArtistId)

        return results

    @staticmethod
    def getTracksForArtist(artistId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select t.TrackId
                from track t, album al
                where t.AlbumId = al.AlbumId
                and al.ArtistId = %s
                """

        cursor.execute(query, (artistId,))

        for row in cursor:
            results.append(row["TrackId"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArtistPlaylistPairs():
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct art.ArtistId, pt.PlaylistId
                from artist art, album al, track t, playlisttrack pt
                where art.ArtistId = al.ArtistId
                and al.AlbumId = t.AlbumId
                and t.TrackId = pt.TrackId
                """

        cursor.execute(query)

        for row in cursor:
            artist_id = row["ArtistId"]
            playlist_id = row["PlaylistId"]
            if artist_id not in results:
                results[artist_id] = []
            results[artist_id].append(playlist_id)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNumAlbumsForArtist(artistId):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """
                select count(distinct al.AlbumId) as NumAlbums
                from album al
                where al.ArtistId = %s
                """

        cursor.execute(query, (artistId,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row["NumAlbums"] if row else 0
