from go_test.grpc.jsonclient import JSONClient
import subprocess

independent_process = subprocess.Popen(
    'server1.exe',
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
)


def runread():
    rpc = JSONClient(("localhost", 1234))

    for i in range(100):
        print(rpc.call("RPCFunc.Echo", "hello " + str(i)))
