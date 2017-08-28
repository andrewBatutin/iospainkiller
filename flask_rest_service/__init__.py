from flask import Flask
from flask_restful import Api
from flask_rest_service.image_processor import ImageIosiphier

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/icon', methods=['POST'])
def process_icon():
    imp = ImageIosiphier()
    return imp.do_stuff("IconsContents.json")

#LaunchImage
@app.route('/splash', methods=['POST'])
def process_splash():
    imp = ImageIosiphier()
    return imp.do_stuff("SplashContents.json")
