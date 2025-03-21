import db.models as db_models

db_conn = db_models.connect_to_db()
db_conn.create_tables([db_models.Song, db_models.Chart, db_models.Score, db_models.TimelinePost])
