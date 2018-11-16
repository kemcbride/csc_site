from models import connect_to_db, Song, Chart, Score


if __name__ == '__main__':
    db = connect_to_db()
    with db.atomic():
        results = Song.select(Song.title, Chart.title, Score.percent).join(Chart).join(Score).where(Score.percent >= 96.0)

        for thing in results:
            print(thing.title, thing.chart.title, thing.chart.score.percent)
