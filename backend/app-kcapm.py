from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
from os import path
import json
import model
from flask_cors import CORS, cross_origin
from flask_compress import Compress
from datetime import datetime
import confiq

#initalizes a variable app, using __main__ attribute
app = Flask('__main__')



cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Compress(app)


#python decorator: It takes the function directly below it and modifies it
#a single route /, the default "root" of our application.

@app.route('/')  
@cross_origin()
def index():
    # TODO : Use this method for health check
    return confiq.APP_NAME


@app.route('/inputfields', methods=['GET'])
@cross_origin()
def getInputFields():
    ws=model.modelFile()
    inputsFields=model.getInputsFields(ws)
    return  json.dumps(inputsFields)


@app.route('/inputs', methods=['POST', 'GET'])
@cross_origin()
def setInputs():
    try:
        payload = request.get_json(force=True)
        inputsList=payload['data']
        
        ws=model.modelFile()
        model.setInputs(ws,inputsList)
        outputData=model.getOutput(ws)
        # model.setInputs(ws, model.DEFAULT_INPUT)
        
        return jsonify(
                message=f"success: model output",
                category="success",
                data=outputData,
                status=200
                )
    except Exception as e:
        return jsonify({'status': 'fail',
                        'message': str(e) }), 400

#for output button calls sankeyScript.py

# @app.route('/output') 
# def outputFile():
#    exec(open("SankeyScript.py").read())


@app.route('/outputs', methods=['GET']) 
@cross_origin()
def outputFile():
    try:
        model.generateOutput()

        return jsonify(
                message=f"success: model output",
                category="success",
                status=200
                )
    except Exception as e:
        return jsonify({'status': 'fail',
                        'message': str(e) }), 400


#This starts the development server for Flask and allows us to visit our web application from our local machine by visiting the localhost.

if __name__ == "__main__":
    app.run(debug= confiq.DEBUG, host= confiq.SERVER_HOST, port= confiq.SERVER_PORT, threaded=True) 








#Using different @app.route calls, we can 'trigger' different parts of the code when the user visits different parts of our application.