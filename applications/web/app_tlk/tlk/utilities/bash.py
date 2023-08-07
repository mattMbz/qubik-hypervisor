import subprocess, os


def welcome():
    print("TLK is an interface. You can use TLK to communicate python with Linux OS, through Bash or Ansible")
## end def


def version():
    print("version 1.0.0")
## end def


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
## end def


## Run bash files
def executeAllPath(path):
    pass
## end def
