from flask import Flask, request, render_template
import inputScript
import requests

API_KEY = ""


def get_prediction_ibm(values):
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,
                                                                                     "grant_type": 'urn:ibm:params'
                                                                                                   ':oauth:grant-type'
                                                                                                   ':apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [['having_IPhaving_IP_Address', 'URLURL_Length',
                                                  'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting',
                                                  'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
                                                  'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token',
                                                  'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH',
                                                  'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover',
                                                  'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord',
                                                  'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page',
                                                  'Statistical_report']], "values": [values]}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4a9dc193-0a81-4b5a-8675-a4c8291a818c/predictions?version'
        '=2022-11-19',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    return response_scoring.json()['predictions'][0]['values'][0][0]


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict')
def predict():
    return render_template('index.html')


success = ""
failure = ""


@app.route('/y_predict', methods=['POST'])
def y_predict():
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    prediction = get_prediction_ibm(checkprediction[0])
    if prediction == 1:
        pred = "This is a legitimate Website. You are Safe!"
        return render_template('index.html', success=pred)

    else:
        pred = "This website looks suspicious. Be cautious!"
        return render_template('index.html', failure=pred)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
