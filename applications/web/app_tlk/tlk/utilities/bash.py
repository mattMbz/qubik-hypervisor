import subprocess, os


def welcome():
    print("TLK is an interface. You can use TLK to communicate python with Linux OS, through Bash or Ansible")


def version():
    print("version 1.0.0")


def executeFile(path, filename , *params):
    path_script = os.path.join(path, filename)
        
    command = ['bash', path_script]
    for param in params:
        command.append(param)
    
    print(command)   
    os.chdir(path)

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f'msg -> {result.stdout.decode()}')

    except subprocess.CalledProcessError as error:
        #catch error and show output code and error message
        print(f"code -> Output code: {error.returncode}")
        print(f"error_msg -> Error message: {error.stderr.decode()}")


def executeFileWithReturn(path, filename, *params):
    path_script = os.path.join(path, filename)
        
    command = ['bash', path_script]
    for param in params:
        command.append(param)
    
    os.chdir(path)

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode()

    except subprocess.CalledProcessError as error:
        #catch error and show output code and error message
        return f"ERROR: {error.returncode}"


## Run bash files
def executeAllPath(path):
    # It's not created yet
    pass
