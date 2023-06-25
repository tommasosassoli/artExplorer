import sqlite3
import definitions
from art.artwork import Association, Artwork


connection = None


def get_connection_and_cursor():
    global connection
    if connection is None:
        connection = sqlite3.connect(definitions.DB_PATH)
    return connection, connection.cursor()


def insert(artwork: Artwork, assoc_list: list[Association]):
    con, cur = get_connection_and_cursor()

    data = (artwork.get_artpedia_id(), artwork.get_description())
    cur.execute("INSERT INTO Artwork VALUES (?, ?)", data)

    data = []
    for assoc in assoc_list:
        d = [artwork.get_artpedia_id()] + assoc.bbox + assoc.tbox
        data.append(d)

    cur.executemany("INSERT INTO Association VALUES(?, ?, ?, ?, ?, ?, ?)", data)
    con.commit()


def select(artwork: Artwork) -> list[Association]:
    con, cur = get_connection_and_cursor()

    # Artwork
    res = cur.execute("""
        SELECT description
        FROM Artwork
        WHERE artpediaId == ?
    """, [artwork.get_artpedia_id()])

    obj = res.fetchone()
    artwork.set_description(obj[0])

    res = cur.execute("""
        SELECT startX, startY, endX, endY, startCh, endCh
        FROM Association
        WHERE artworkId == ?
    """, [artwork.get_artpedia_id()])

    assoc_list = []
    for row in res:
        bbox = list(row[0:4])
        tbox = list(row[4:6])
        assoc_list.append(Association(bbox, tbox))

    return assoc_list

