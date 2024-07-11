from bottle import Bottle, template, static_file, request
from canvas import AnnotatedCanvas
import bottle_session

app = Bottle()
plugin = bottle_session.SessionPlugin(cookie_lifetime=6000)
app.install(plugin)

@app.route('/', method='GET')
def index():
    canvas = request.query.get(
        'iiif-image',
        'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1'
    )
    return template('index', data=canvas)

@app.route('/', method='POST')
def submit():
    field_data = request.forms.get('annotation_url')
    print(field_data)
    canvas = request.query.get(
        'iiif-image',
        'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1'
    )
    return template('index', data=canvas)

@app.route('/cropper')
def cropper():
    canvas = request.query.get(
        'baseUrl',
        'https://api.library.tamu.edu/iiif/2/f10c7823-4e52-334d-829a-239b69b9f81d;1'
    )
    return template('static/cropper', data=canvas)

@app.route('/map')
def cropper():
    return template('static/map')

@app.route('/static/styles.css')
def static_styles():
    return static_file('styles.css', root='./views/static')

@app.route('/static/app.js')
def serve_app_js():
    return static_file('app.js', root='./views/static')


if __name__ == '__main__':
    app.run(debug=True, reloader=True)
