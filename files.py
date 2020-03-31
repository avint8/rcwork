from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import alg


ALLOWED_EXTENSIONS = {'tiff'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


	
@app.route('/', methods = ['GET', 'POST'])
def up():

   if request.method == 'POST':
         if 'file' not in request.files:
            im=0
         option=request.form['option']
         f = request.files['file']
         
         if f.filename == '':
            im=0

         if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)

            if option=='e':
               f.save('static/'+'img.tiff')
               alg.encrypt()
               return render_template('upload.html',im=1,op=option)
            elif option=='d':
               f.save('static/'+'enimg.tiff')
               alg.decrypt()
               return render_template('upload.html',im=1,op=option)
         
   return render_template('upload.html',im=0)


if __name__ == '__main__':
   app.run(threaded=Tree, port= 5000)