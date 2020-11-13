from flask import Flask,render_template,url_for,request
import pandas as pd
import pickle
import json
import os
#import urllib.request
import urllib2
import json


app= Flask(__name__,static_folder="static")


#Define a view function named 'home', which renders the html page 'home.html'
#Ensure that the view function 'home' is routed when a user access the URL '/' .

@app.route('/')
def home():
	return render_template('index.html')



#Define a view function named 'predict', which does the function of getting the text entered by user in home.html and predicts if it is spam or not and renders the result in result.html
#Ensure that the view function 'predict' is routed when a user access the URL '/predict' .




@app.route('/predict',methods=['POST'])
def predict():
	
	
	data = {
        "Inputs": {
                "input1":
                [
                    {
                            'text': request.form['message'],   
                            
                    }
                ],
        },
		"GlobalParameters":  {
							}
	}

	body = str.encode(json.dumps(data))
	print(data)
	url = 'https://ussouthcentral.services.azureml.net/workspaces/cb42094b240f4bdd94e35c93616c410e/services/b35a822d95804870adbd49da925f6f74/execute?api-version=2.0&format=swagger'
	api_key = 'ljmUH0k0X4Yu8ooYEI10+09JiUwzi569UET1pDKnjsefl+dxt4XCaBoVEdeagK3y2m0Q8Vp3Z4IUaUqTRVvDBQ==' # Replace this with the API key for the web service
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	req = urllib2.Request(url, body, headers)
	response = urllib2.urlopen(req)
	#req = urllib.request.Request(url, body, headers)
	#response = urllib.request.urlopen(req)
	#result = response.read().decode('utf-8')
	result = response.read()
	print(result)
	y = json.loads(result)
	print(y['Results']['output1'][0]['Scored Labels'])
	y = json.loads(result)
	prediction_value=y['Results']['output1'][0]['Scored Labels']
	if prediction_value=="1":
		prediction_text="Negative"
	elif prediction_value=="3":
		prediction_text="Moderate"
	elif prediction_value=="5":
		prediction_text="Positive"
	else:
		prediction_text="Irrelevant Tweet"
	
	
	print(prediction_text)
		
	
		
	return render_template('result.html',prediction = prediction_text)



	
		






# make your app run in 0.0.0.0 host and port 8000
if __name__ == '__main__':
	app.run(debug=True)
	#app.run('0.0.0.0',port=8000,debug=True)
