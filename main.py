import random
from functools import wraps
from flask import Flask, send_file
from flask import render_template
from flask import request
from tools import sm3_dgst, sm4_cbc_encrypt, sm4_cbc_decrypt, sm2_verify, sm2_sign
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
def check_param(param_name):
    """
    装饰器，⽤于检查请求参数是否存在
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            param_value = request.form.get(param_name)
            if param_value is None:
                return f"Error: '{param_name}' parameter is missing", 400
            else:
                return func(param_value, *args, **kwargs)
        return wrapper
    return decorator
@app.route('/sm4_cbc_encrypt', methods=['POST'])
@check_param('msg')
@check_param('key')
def sm4_cbc_encrypt_endpoint(key, msg):
    return sm4_cbc_encrypt(msg, key)


@app.route('/sm4_cbc_decrypt', methods=['POST'])
@check_param('msg')
@check_param('key')
def sm4_cbc_decrypt_endpoint(key, msg):
    return sm4_cbc_decrypt(msg, key)


@app.route('/sm3_dgst', methods=['POST'])
@check_param('msg')
def sm3_dgst_endpoint(msg):
    return sm3_dgst(msg)
@app.route('/sm2_sign', methods=['POST'])
@check_param('path')
def sm2_sign_endpoint(path):
    sign_file = path + '_sign'
    sm2_sign(path, sign_file)
    return {'path': sign_file}
@app.route('/sm2_verify', methods=['POST'])
@check_param('file_path')
@check_param('sign_file_path')
def sm2_verify_endpoint(sign_file_path, file_path):
    return sm2_verify(sign_file_path, file_path)
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    random_num = str(random.randint(10000, 99999))
    filename = file.filename
    new_filename = random_num + '_' + filename
    save_path = './file/' + new_filename
    file.save(save_path)
    return {'path': save_path}


@app.route('/download', methods=['POST'])
@check_param('file_path')
def download_file(file_path):
    return send_file(file_path, as_attachment=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)