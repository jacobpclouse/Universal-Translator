# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify
import os

app = Flask(__name__)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-




# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
@app.route('/',methods=['GET', 'POST'])
def translate():
    dashboardHeader = "Speech to Speech" # in base temp, basically what this page does
    title = "Speech to Speech - Jacob Clouse Universal Translator" # in base temp, actual page title in browser
    
    if request.method == 'POST':
        app.logger.debug(request.files['file'].filename) 
        # files = request.files
        # file = files.get('file')
        # print(file)

        # with open(os.path.abspath(f'./UPLOADS/output.wav'), 'wb') as f:
        #     f.write(file.content)

        # response = jsonify("File received and saved!")
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # 
        audio = request.data  
        print(audio)    
        with open(os.path.abspath(f'./UPLOADS/output.wav'), 'wb') as f:
            f.write(audio)
    return render_template('translate.html', html_title = title, dash_head = dashboardHeader)



# main statement - used to set dev mode
if __name__ == '__main__':
    app.run(debug=True)