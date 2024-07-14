from bottle import Bottle, template, static_file, request
from beaker.middleware import SessionMiddleware
from feature import Feature

session_opts = {
    'session.type': 'file',
    'session.data_dir': './.cache',
    'session.auto': True,
    'session.cookie_expires': 600
}

app = Bottle()

@app.hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

@app.route('/', method='GET')
def index():
    if 'annotations' not in request.session:
        request.session['annotations'] = []
    canvas = request.query.get(
        'iiif-image',
        'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1'
    )
    print(request.session['annotations'])
    return template('index', data=canvas)

@app.route('/', method='POST')
def submit():
    if 'annotations' not in request.session:
        request.session['annotations'] = []
    form_data = {
        "iiif_map_image": request.forms.get('iiif_map_image'),
        "canvas_url": request.forms.get('canvas_url'),
        "image_points": request.forms.get('image_points'),
        "image_region": request.forms.get('image_region'),
        "latitude": request.forms.get('latitude'),
        "longitude": request.forms.get('longitude'),
        "annotation_label": request.forms.get('annotation_label'),
        "annotation_tags": request.forms.get('annotation_tags'),
        "annotation_url": request.forms.get('annotation_url'),
    }
    request.session['annotations'].append(Feature(form_data).build())
    request.session.save()
    canvas = request.query.get(
        'iiif-image',
        'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1'
    )
    print(request.session['annotations'])
    return template('index', data=canvas)

@app.route('/cropper')
def cropper():
    canvas = request.query.get(
        'baseUrl',
        'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1'
    )
    return template('static/cropper', data=canvas)

@app.route('/map')
def map_view():
    return template('static/map')

@app.route('/static/styles.css')
def static_styles():
    return static_file('styles.css', root='./views/static')

@app.route('/static/app.js')
def serve_app_js():
    return static_file('app.js', root='./views/static')

app = SessionMiddleware(app, session_opts)


if __name__ == '__main__':
    from bottle import run
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)
