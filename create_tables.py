from db.models import Song, Chart, Score, MYSQL_DB

if __name__ == '__main__':
    with MYSQL_DB.atomic():
        MYSQL_DB.create_tables([Song, Chart, Score])
