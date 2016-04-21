import subprocess
from io import BytesIO


def run(command_args, input_data=None):
    if input_data and not hasattr(input_data, 'read'):
        input_data = open(input_data, 'rb')

    if input_data:
        process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_data, stderr_data = process.communicate(input=input_data.read())
        stdout_data = BytesIO(stdout_data)
    else:
        process = subprocess.Popen(command_args, stdout=subprocess.PIPE)
        stdout_data, stderr_data = process.communicate()
        stdout_data = BytesIO(stdout_data)

    if hasattr(input_data, 'close'):
        input_data.close()

    return stdout_data
