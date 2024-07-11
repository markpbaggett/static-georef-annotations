from bottle import Bottle, template, static_file

app = Bottle()

@app.route('/')
def index():
    return template('index')

@app.route('/cropper')
def cropper():
    return template('static/cropper')

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
