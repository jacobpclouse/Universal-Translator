# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory


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
        print(request.data)
        f = open('./UPLOADS/file1.wav', 'wb')
        f.write(request.data)
        f.close()
    
    
    return render_template('translate.html', html_title = title, dash_head = dashboardHeader)



# main statement - used to set dev mode
if __name__ == '__main__':
    app.run(debug=True)