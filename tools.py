import subprocess

# SM4-CBC加密
def sm4_cbc_encrypt(plaintext: str, key: str):
    command = 'echo ' + plaintext + ' | /opt/tongsuo/bin/tongsuo enc -K ' + key + ' -e -sm4-cbc ' \
'-iv 1fb2d42fb36e2e88a220b04f2e49aa13 -nosalt -base64',
    return shell(command)
# SM4-CBC解密
def sm4_cbc_decrypt(ciphertext: str, key: str):
    command = 'echo ' + ciphertext + '| /opt/tongsuo/bin/tongsuo enc -K '+key+' -d -sm4-cbc ' \
'-iv 1fb2d42fb36e2e88a220b04f2e49aa13 -nosalt -base64'
    return shell(command)
# sm3杂凑算法
def sm3_dgst(ciphertext: str):
    command = 'echo -n ' + ciphertext + ' | /opt/tongsuo/bin/tongsuo dgst -sm3'
    return shell(command)
# sm2签名验证
def sm2_verify(sig_file: str, file_path: str):
    command = "/opt/tongsuo/bin/tongsuo dgst -sm3 -verify ./sm2pub.key -signature {} {}".format(sig_file, file_path)
    return shell(command)
# sm2 签名
def sm2_sign(file_path: str, sig_file: str):
    command = "/opt/tongsuo/bin/tongsuo dgst -sm3 -sign ./sm2.key -out {} {}".format(sig_file, file_path)
    return shell(command)
def shell(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    # 获取命令的输出和错误信息
    output = process.stdout.read()
    error = process.stderr.read()
    # 将输出和错误信息解码为字符串
    output = output.decode(encoding="utf8")
    error = error.decode(encoding="utf8")
    # 返回命令的输出和错误信息
    result = {"output": output, "error": error}
    print(result)
    return result