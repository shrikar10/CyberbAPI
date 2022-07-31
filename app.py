from flask import Flask, request
from flask_cors import CORS,cross_origin
import pickle
from googletrans import Translator
from flasgger import Swagger
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Swagger(app)
pred = pickle.load(open('model.pkl', 'rb'))

def translate(comment):
  translator = Translator()
  comment = translator.translate(comment,lang_code='en').text
  print(comment)
  return comment
@app.route('/')
def welcome():
    return "Welcome"


@app.route('/predict', methods=["GET"])
def predict_text():
    """Let's classify these comments
    This is using docstrings for specifications.
    ---
    parameters:
      - name: tweet
        in: query
        type: string
        required: true
    responses:
      200:
        description: Succesfully classified   
    """
    tweet = request.args.get('tweet')
    tweet = translate(tweet)
    
    predict_t = pred.predict([tweet])
    return str(predict_t[0]) 
    #"The prediction output is " + 

@app.route('/predict_api',methods =["POST"])
@cross_origin()
def predict_api():
    """Let's classify these comments
    This is using docstrings for specifications.
    ---
    parameters:
      - name: tweet
        in: body
        type: string
        required: true
    responses:
      200:
        description: Succesfully classified   
    """
    data = request.get_json(force=True)
    tweet = data["tweet"]
    tweet = translate(tweet)
    predict_t = pred.predict([tweet])
    return str(predict_t[0])
if __name__ == '__main__':
    app.run()
