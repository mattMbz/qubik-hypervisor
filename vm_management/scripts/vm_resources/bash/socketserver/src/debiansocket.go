package main

import (
	"fmt"
	"net"
	"os/exec"
	"path/filepath"
	"strings"
)

const (
	SERVER_PORT = "8503"
	SERVER_TYPE = "tcp"
)

func runBash(scriptname string) (string, error) {
	// Relative path to the Bash script.
	relativePath := fmt.Sprintf("../../%s", scriptname)

	// Get the absolute path to the script.
	absPath, err := filepath.Abs(relativePath)
	if err != nil {
		return "", err
	}

	// Command to execute the Bash script.
	cmd := exec.Command("bash", absPath)

	// Execute the command and capture the output.
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}

	// Convert the output into a text string.
	outputStr := string(output)
	return outputStr, nil
}

func readCPU() (string, error) {
	getcpuinfo := "cpuinfo.sh"
	cpuInfo, err := runBash(getcpuinfo)
	cpuInfo = strings.TrimSpace(cpuInfo)
	if err != nil {
		return "", err
	}
	return cpuInfo, nil
}

func readVCPU() (string, error) {
	getcpuinfo := "cpu_normalized_info.sh"
	cpuInfo, err := runBash(getcpuinfo)
	cpuInfo = strings.TrimSpace(cpuInfo)
	if err != nil {
		return "", err
	}
	return cpuInfo, nil
}

func readMemory() (string, error) {
	getMemoryInfo := "memoryinfo.sh"
	memoryInfo, err := runBash(getMemoryInfo)
	memoryInfo = strings.TrimSpace(memoryInfo)
	if err != nil {
		return "", err
	}
	return memoryInfo, nil
}

func readDisk() (string, error) {
	getDiskInfo := "diskinfo.sh"
	diskInfo, err := runBash(getDiskInfo)
	diskInfo = strings.TrimSpace(diskInfo)
	if err != nil {
		return "", err
	}
	return diskInfo, nil
}

func readAll() (string, error) {
	return "reading all resources !!!", nil
}


func handleConnection(conn net.Conn) {
	defer conn.Close()

	buffer := make([]byte, 1024)

	for {
		n, err := conn.Read(buffer)
		if err != nil {
			fmt.Println(err)
			return
		}

		data := string(buffer[:n])

		var response string
		switch data {
		case "cpu":
			response, err = readVCPU()
		case "memory":
			response, err = readMemory()
		case "disk":
			response, err = readDisk()
		case "all":
			response, err = readAll()
		default:
			response = "Invalid request"
		}

		if err != nil {
			fmt.Println(err)
			response = "Error occurred"
		}

		_, err = conn.Write([]byte(response))
		if err != nil {
			fmt.Println(err)
			return
		}
	}
}


func main() {

	scriptname := "host_ip_address.sh"
	ipaddr, err := runBash(scriptname)
	ipaddr = strings.TrimSpace(ipaddr) //Clean up white spaces.

	if err != nil {
		fmt.Println(err)
		return
	}

	server, err := net.Listen(SERVER_TYPE, ipaddr+":"+SERVER_PORT)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer server.Close()

	fmt.Println("Listening in host " + ipaddr + " on port " + SERVER_PORT)

	for {
		conn, err := server.Accept()
		if err != nil {
			fmt.Println(err)
			continue
		}

		go handleConnection(conn)
	}
}
