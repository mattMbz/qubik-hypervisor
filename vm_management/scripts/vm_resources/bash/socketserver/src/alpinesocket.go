package main

import (
	"fmt"
	"io/ioutil"
	"time"
	"strings"
	"strconv"
	"os/exec"
	"net"
)

const (
	SERVER_PORT = "8503"
	SERVER_TYPE = "tcp"
)

func getDiskInfo() (string, error) {
	cmd := exec.Command("df", "/")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println("Error al ejecutar el comando:", err)
		return "", err
	}

	lines := strings.Split(string(output), "\n")
	if len(lines) < 2 {
		fmt.Println("Error: No se pudo obtener la información del disco")
		return "", err
	}

	fields := strings.Fields(lines[1])
	if len(fields) < 6 {
		fmt.Println("Error: No se pudieron extraer los campos de la salida")
		return "", err
	}

	fileSystem := fields[0]
	size := fields[1]
	used := fields[2]
	available := fields[3]
	percentage := strings.Replace(fields[4], "%", "", -1)
	mounted := fields[5]

	diskPythonDict := fmt.Sprintf("{'size': '" + humanize(size) + "', 'used': '" + humanize(used) + "', 'available': '" + humanize(available) + "', 'percentage': '" + percentage + "', 'mounted': '" + mounted + "', 'filesystem': '"+fileSystem+"'}")

	return diskPythonDict, nil
}

func readMemInfo(memType string) string {
	var memorySize []string
	var memorySizeValue string

	// Read "/proc/meminfo" file
	cmd := exec.Command("more", "/proc/meminfo")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println(err)
	}
	lines := strings.Split(string(output), "\n")

	for _, line := range lines {
		if strings.Contains(line, memType){
			memorySize = strings.Split(line, ":")
			memorySizeValue = strings.TrimSpace(memorySize[1])
			memorySizeValue = strings.TrimSuffix(memorySizeValue, " kB")
			break
		}
	}

	return memorySizeValue

}


func humanize(value string) string {
    /** Function to convert value to human-readable format */

	floatValue, _ := strconv.ParseFloat(value, 64)
	length := len(value)

	if length > 6 {
		gb := floatValue / (1024 * 1024)
		roundedValue := fmt.Sprintf("%.2f", gb)
		return roundedValue + " GB"
	} else if length >= 4 && length <= 6 {
		mb := floatValue / 1024
		roundedValue := fmt.Sprintf("%.2f", mb)
		return roundedValue + " MB"
	} else {
		roundedValue := fmt.Sprintf("%.2f", floatValue)
		return roundedValue + " KB"
	}
}


func getMemoryInfo() (string, error) {

	//total:=readMemInfo("MemTotal")
	freeStr:=readMemInfo("MemFree")
	buffersStr:=readMemInfo("Buffers")
	availableStr:=readMemInfo("MemTotal")
	cachedStr:=readMemInfo("Cached")
	KReclaimableStr:=readMemInfo("KReclaimable")
	hugepagesizeStr:=readMemInfo("Hugepagesize")
	pageTablesStr:=readMemInfo("PageTables")
	kernelStackStr:=readMemInfo("KernelStack")

	//memTotal, err := strconv.Atoi(total)
	freeInt, err := strconv.Atoi(freeStr)
	buffersInt, err := strconv.Atoi(buffersStr)
	availableInt, err := strconv.Atoi(availableStr)
	cachedInt, err := strconv.Atoi(cachedStr)
	KReclaimableInt, err := strconv.Atoi(KReclaimableStr)
	hugepagesizeInt, err := strconv.Atoi(hugepagesizeStr)
	pageTablesInt, err := strconv.Atoi(pageTablesStr)
	kernellStackInt, err := strconv.Atoi(kernelStackStr)

	if(err != nil) {
		fmt.Println(err)
		return "", err
	}

	// Calculate mem_used
	usedInt := availableInt - freeInt - buffersInt - cachedInt - KReclaimableInt - hugepagesizeInt - pageTablesInt - kernellStackInt

	// Calculate percentage
	percentage := (usedInt * 100) / availableInt
	
	// Convert values to human-readable format
	usedHuman := humanize(strconv.Itoa(usedInt))
	availableHuman := humanize(availableStr)
	freeHuman := humanize(freeStr)

	usedPercentage := strconv.Itoa(percentage)

	memoryPythonDict := fmt.Sprintf("{'percentage': '" + usedPercentage + "', 'Total': '" + availableHuman + "', 'Used': '" + usedHuman + "', 'Free': '" + freeHuman + "'}")

	return memoryPythonDict, nil
}


func readCPUCores() (string, error){
	/** Reading the Linux CPU cores information from /proc/cpuinfo file */

	// Execute the command and catch the output
	cmd := exec.Command("cat", "/proc/cpuinfo")
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}

	// Contar las líneas que contienen "processor"
	processorCount := 0
	lines := strings.Split(string(output), "\n")
	for _, line := range lines {
		if strings.Contains(line, "processor") {
			processorCount++
		}
	}

	return strconv.Itoa(processorCount), err
}


// Reading the Linux /proc/stat file 
func readProcStat() (map[string][]string, error) {
	number, err := readCPUCores()
	cpuNumbers, err := strconv.Atoi(number)
	if err != nil {
		fmt.Println("Error al convertir el string a int:", err)
	}

	procStatFile, err := ioutil.ReadFile("/proc/stat")
	if err != nil {
		fmt.Println("Error reading /proc/stat:", err)
	}

	procStatInfo := string(procStatFile)

	coresLine := []string {}
	lines := strings.Split(procStatInfo, "\n")
	

	for n:=0; n < cpuNumbers; n++ {
		for _, line := range lines {
			if strings.Contains(line, "cpu"+strconv.Itoa(n) ) {
				coresLine = append(coresLine, line)
				break
			}
		}
	}

	cpuValues := make(map[string][]string)

	for i:=0; i < len(coresLine); i++ {
		cpuArray := strings.Split(coresLine[i]," ")
		cpuValues["cpu"+strconv.Itoa(i)] = cpuArray
	}

	return cpuValues, err
}


// Calculating usage CPU % percentage
func getCPUInfo() (string, error) {
	var systemTime1 int
	var idleTime1 int
	var systemTimesArray1 []int
	var idleTimesArray1 []int

	var systemTime2 int
	var idleTime2 int
	var systemTimesArray2 []int
	var idleTimesArray2 []int

	var deltaCpuIdle int
	var deltaCpuSystem int
	var totalCpuTime int
	var cpuUsageArray []string

	cpuTimesOne, err := readProcStat()
	time.Sleep(500 * time.Millisecond)
	cpuTimesTwo, err := readProcStat()

	if err != nil {
		fmt.Println("Error: ", err)
		return "", err
	} 

	for i:=0; i < len(cpuTimesOne); i++ {
		systemTime1, _ = strconv.Atoi( cpuTimesOne["cpu"+strconv.Itoa(i)][3] )
		idleTime1, _ = strconv.Atoi( cpuTimesOne["cpu"+strconv.Itoa(i)][4] )
		systemTimesArray1 = append(systemTimesArray1, systemTime1)
		idleTimesArray1 = append(idleTimesArray1, idleTime1)

		systemTime2, _ = strconv.Atoi( cpuTimesTwo["cpu"+strconv.Itoa(i)][3] )
		idleTime2, _ = strconv.Atoi( cpuTimesTwo["cpu"+strconv.Itoa(i)][4] )
		systemTimesArray2 = append(systemTimesArray2, systemTime2)
		idleTimesArray2 = append(idleTimesArray2, idleTime2)
	}

	for i:= 0; i < len(idleTimesArray1); i++ {
		deltaCpuIdle = idleTimesArray2[i] - idleTimesArray1[i]
		deltaCpuSystem = systemTimesArray2[i] - systemTimesArray1[i]
		totalCpuTime = deltaCpuIdle + deltaCpuSystem 
		percentage := (1 - (float64(deltaCpuIdle)/float64(totalCpuTime)))* 100
		cpuUsageArray = append(cpuUsageArray, strconv.FormatFloat(percentage, 'f', 2, 64))
	}

	cpuPythonDict := "{ "
	end := "}"

	for i := 0; i < len(cpuUsageArray); i++ {
		cpuPythonDict = cpuPythonDict+"'"+"cpu"+strconv.Itoa(i)+"':'"+cpuUsageArray[i]+"',"
	}
	cpuPythonDict = cpuPythonDict + end

	return cpuPythonDict, nil	
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
			response, err = getCPUInfo()
		case "memory":
			response, err = getMemoryInfo()
		case "disk":
			response, err = getDiskInfo()
		// case "all":
		// 	response, err = readAll()
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

func getIpAddr(ifaceName string) (string, error) {
	iface, err := net.InterfaceByName(ifaceName)
	if err != nil {
		return "", err
	}

	addrs, err := iface.Addrs()
	if err != nil {
		return "", err
	}

	// Buscar la primera dirección IP válida de la interfaz de red
	for _, addr := range addrs {
		ipnet, ok := addr.(*net.IPNet)
		if ok && !ipnet.IP.IsLoopback() && ipnet.IP.To4() != nil {
			return ipnet.IP.String(), nil
		}
	}

	return "", fmt.Errorf("No se encontró una dirección IP válida para la interfaz de red %s", ifaceName)
}

func main() {

	ifaceName := "eth0"
	//ifaceName := "enp0s3"
	ipaddr, err := getIpAddr(ifaceName)
	if err != nil {
		fmt.Printf("Error al obtener la dirección IP de %s: %s\n", ifaceName, err)
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
