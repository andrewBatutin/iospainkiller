from flask import Flask
from flask_restful import Api
from flask_rest_service.image_processor import ImageIosiphier

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/', methods=['POST'])
def process_image():
    imp = ImageIosiphier()
    return imp.do_stuff()