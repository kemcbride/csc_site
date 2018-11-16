STATIC_PATH = 'static'
KODONODO_DIRS = [
    'handrawn',
    'kelly_pics',
]


def linkify(filename, path, https=False):
    return 'http{}://csclub.uwaterloo.ca/~ke2mcbri/{}/{}'.format(
        's' if https else '',
        path,
        filename
    )


def make_static_config(static_dir):
    path = '/'.join([STATIC_PATH, static_dir])
    cfg = {
        path : {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': path,
        }
    }
    return cfg
