![qubik](https://i.imgur.com/qx3daI8.png)

[![Version](https://img.shields.io/badge/version-0.8-blue.svg)](https://semver.org)

Qubik is a project for turning your Linux server into a hypervisor and running virtual machines. Written in bash scripting for controlling virtual machines and Django framework for providing the user with a remote management web application. This project incorporates open source virtualization technologies such as libvirt, qemu, and KVM. It's been inspired by other cloud hypervisors like Digital Ocean.

## Features
- Turn your Linux server into a Hypervisor and manage virtual machines from your browser.
- Create, run, stop and delete virtual machine from your web browser.
- Run Debian and Alpine Linux virtual machines from the Qubik web hypervisor.
- Resources monitoring for the hypervisor like as CPU, Memory and Disks usage.
- Resources monitoring for vm like as CPU, Memory and Disks usage.
- Automatic application deployment.
- At the moment, new functionalities are creating 🚀 ...

## Table of Contents

- [Core technologies](#core-technologies)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Core technologies

| Technology | Description | Version |
| ------ | ------ | ------ |
| Python     | The main programming language for this project. |  3.9.2  |
| Django     | Web development framework. |  3.2.16  |
| TypeScript | Is a typed superset of JavaScript, used for frontend. |  5.1.6  |
| Go         | Efficiency and concurrency, used to implement resource monitor.|  1.19.10  |
| Gunicorn   | HTTP WSGI server for Python. | 21.2.0 |
| Uvicorn    | ASGI server that allows running Python web applications asynchronously. | 0.23.2 |
| Bash       | Used on operating systems for task automation. |  5.1.4  |
| Libvirt    | An API and toolset for managing virtual machines. |  7.0  |
| QEMU       | An open-source emulator and virtualizer. |  5.2.0  |
| KVM        | A kernel module in Linux that provides virtualization capabilities for running virtual machines. |  5.2.0  |

## Architecture

The architecture of this hypervisor is configured in different layers. It starts with an application layer where a frontend connects with a backend. Then, the layers below the backend/Django correspond to the management of virtual machines and some automation tasks for their configuration.

![architecture](https://i.imgur.com/6u0xoeF.png)

## Installation

### Option 1:  
  
**Clone this repository:** To clone the repository to your local machine, open the terminal and navigate to the directory where you want the repository to be cloned, and run the following command:

```sh
$ mkdir hypervisor
$ cd hypervidor
$ git clone https://github.com/mattMbz/qubik-hypervisor

# Now we'll install Qubik Hypervisor:
$ cd setup/
$ ./install.sh

# Now we'll install python dependences:
$ cd applications/web/
$ pip install -r requirements.txt
```
This will download the entire repository to your local machine.

### Option 2:  
  
**Download as a ZIP file:** If you don't want to clone the entire repository or don't have access to Git on your system, you can download it as a ZIP file. To do this, go to the repository page on GitHub, click the green "Code" button, and then select "Download ZIP". This will download a ZIP file of the repository to your computer. 

```sh
$ unzip example.zip -d /path/to/extract/hypervisor #folder
$ cd hypervisor

# Now we'll install Qubik Hypervisor:
$ cd setup/
$ ./install.sh

# Now we'll install python dependences:
$ cd applications/web/
$ pip install -r requirements.txt
```  
This will download the entire repository to your local machine.

<!-- [Go back](#table-of-contents) -->

<!-- ## Usage

<!-- Explain how to use your project. Provide examples and guides so users can get started quickly.  

<!-- [Go back](#table-of-contents) -->


## License

GNU GENERAL PUBLIC LICENSE

By adopting the GPL 3.0 license, developers can contribute to the growth and advancement of open-source software. This fosters collaborative innovation and allows the software to evolve sustainably, benefiting the community at large.

<!-- [Go back](#table-of-contents) -->


## Contact

Feel free to reach out to me through any of the following channels:

- **Email:** matias.mbz@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/mattmbz/
- **GitHub:** https://github.com/mattMbz
<!-- - **Website:** [Your Personal Website](https://www.yourwebsite.com) -->
