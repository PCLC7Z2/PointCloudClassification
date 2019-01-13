import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploadfiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 设置上传最大长度16M
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def welcome():
	return 'hello!!!'


# 上传文件
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # print(f.filename)
        if f and allowed_file(f.filename):
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'uploadfiles',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            print(upload_path)
            return redirect(url_for('upload'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# 查看当前上传文件
from flask import send_from_directory
@app.route('/uploadfiles/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
	app.run('127.0.0.1', 1001)
