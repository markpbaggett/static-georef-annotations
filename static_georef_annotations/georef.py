from bottle import Bottle, template, static_file, request
from beaker.middleware import SessionMiddleware
from feature import Feature
from canvas import AnnotatedCanvas
import json

session_opts = {
    'session.type': 'file',
    'session.data_dir': './.cache',
    'session.auto': True,
    'session.cookie_expires': 6000,
    'session.annotations': [],
    'session.canvas': 'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1',
    'session.canvas_label': '',
    'session.canvas_id': ''
}

app = Bottle()

@app.hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

@app.route('/', method='GET')
def index():
    canvas = request.query.get(
        'iiif-image',
        session_opts.get('session.canvas')
    )
    request.session['canvas'] = canvas
    request.session.save()
    return template('index', data=canvas, canvas=request.session['canvas'])

@app.route('/', method='POST')
def submit():
    if 'annotations' not in request.session:
        request.session['annotations'] = []
    if 'canvas' not in request.session:
        request.session['canvas'] = request.forms.get('iiif_map_image')
    request.session['canvas_label'] = request.forms.get('canvas_label')
    request.session['canvas_id'] = request.forms.get('canvas_url')
    form_data = {
        "iiif_map_image": request.forms.get('iiif_map_image'),
        "canvas_label": request.forms.get('canvas_label'),
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
    return template('index', data=request.session['canvas'], canvas=request.session['canvas'])

@app.route('/generate', method='GET')
def generate():
    for key, value in request.session.items():
        # Debugging help to figure out what's in the session
        print(f"{key}: {value}")
    if len(session_opts['session.annotations']) == 0:
        annotated_canvas = AnnotatedCanvas(
            request.session['canvas'],
            annotations=request.session['annotations'],
            canvas_label=request.session['canvas_label'],
            canvas_id=request.session['canvas_id'],
        )
        annotated_canvas_without_features = annotated_canvas.build()
        if 'annotations' in annotated_canvas_without_features:
            annotated_canvas_without_features['annotations'][0]['items'][0]['body']['features'] = session_opts['session.annotations']
        return template(
            'generate',
            data=json.dumps(
                annotated_canvas_without_features,
                indent=4
            ),
            canvas=request.session['canvas'],
        )
    else:
        return template(
            'generate',
            data='No annotations or session expired.',
            canvas=request.session['canvas'],
        )


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
