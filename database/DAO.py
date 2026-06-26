from database.DB_connect import DBConnect
from model.Actor import Actor


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getRating():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct avg_rating 
                from ratings 
                order by avg_rating """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(rate1, rate2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct  n.id, n.name, n.height, n.date_of_birth , n.known_for_movies 
                    from names n , role_mapping rm , movie m , ratings r 
                    where n.id  = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
                    and r.avg_rating >= %s and r.avg_rating <= %s
                    and n.date_of_birth is not null"""

        cursor.execute(query, (rate1,rate2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllEdges(rate1, rate2):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select  distinct act1.id as a1, act2.id as a2
                    from  (select distinct  n.name , n.id , m.id as film, m.worlwide_gross_income as incasso
                    from names n , role_mapping rm , movie m , ratings r 
                    where n.id  = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
                    and r.avg_rating >= %s and r.avg_rating <= %s
                    and n.date_of_birth is not null
                    and m.worlwide_gross_income is not null) as act1, 
                    (select distinct  n.name , n.id , m.id as film, m.worlwide_gross_income as incasso
                    from names n , role_mapping rm , movie m , ratings r 
                    where n.id  = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
                    and r.avg_rating >= %s and r.avg_rating <= %s
                    and n.date_of_birth is not null
                    and m.worlwide_gross_income is not null) as act2
                    where act1.film  = act2.film  
                    and act1.id > act2.id
                    group by a1 , a2"""

        cursor.execute(query, (rate1, rate2, rate1, rate2))

        for row in cursor:
            results.append((row["a1"], row["a2"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPesoArco(id1, id2):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT SUM(CAST(REPLACE( REPLACE( REPLACE(m.worlwide_gross_income, '$', ''), ',', ''), ' ', '') AS UNSIGNED)) AS peso
                    FROM role_mapping rm1, role_mapping rm2, movie m
                    WHERE rm1.movie_id = rm2.movie_id 
                    AND rm1.movie_id = m.id
                    AND rm1.name_id = %s 
                    AND rm2.name_id = %s
                    """

        cursor.execute(query, (id1, id2))

        for row in cursor:
            results.append((row["peso"]))

        cursor.close()
        conn.close()
        return results
