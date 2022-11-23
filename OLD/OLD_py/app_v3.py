# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify
import os
import datetime

app = Flask(__name__)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
@app.route('/',methods=['GET', 'POST'])
@app.route('/audioUpload',methods=['GET', 'POST'])
def translate():
    dashboardHeader = "Speech to Speech" # in base temp, basically what this page does
    title = "Speech to Speech - Jacob Clouse Universal Translator" # in base temp, actual page title in browser
    
    if request.method == 'POST':
        # Grab current date & time from function & store in variable
        use_this_datetime = defang_datetime()

        # had issues importing audio data below, used this link to gather data: https://stackoverflow.com/questions/65632555/sending-wav-file-from-frontend-to-flask-backend
        print(request.files)
        data = request.files['audio-file'].read()
        print(data)

        #audio = request.form["audio-file"] # what is the name of form data being sent?
        # files = request.files
        # file = files.get('file')
        # print(file)

        # with open(os.path.abspath(f'./UPLOADS/output.wav'), 'wb') as f:
        #     f.write(file.content)


        # audio = request.data  
        # print(audio)    

        
        # save to file
        with open(os.path.abspath(f'./UPLOADS/output{use_this_datetime}.mp3'), 'wb') as f:
            f.write(data)

    return render_template('translate.html', html_title = title, dash_head = dashboardHeader)



# main statement - used to set dev mode
if __name__ == '__main__':
    app.run(debug=True)