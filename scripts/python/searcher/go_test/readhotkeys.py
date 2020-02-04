
import json
import requests
import subprocess

independent_process = subprocess.Popen(
    'main.exe',
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
)

url = 'http://localhost:8972/'
payload = {
    'A': 15,
    'B': 20
}


def readkeys():
    # Adding empty header as parameters are being sent in payload
    headers = {
        "Host": "localhost",
        "Connection": "keep-alive",
        "X-RPCX-MessageID": "12345678",
        "X-RPCX-MesssageType": "0",
        "X-RPCX-SerializeType": "1",
        "X-RPCX-ServicePath": "Arith",
        "X-RPCX-ServiceMethod": "Mul",
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.content)
