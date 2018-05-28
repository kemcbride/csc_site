import xml.etree.ElementTree as ET

from db.models import Song, Chart, Score, mysql_db

if __name__ == '__main__':
    with mysql_db:

        # Song, Chart, Score
        mysql_db.create_tables([Song, Chart, Score])
