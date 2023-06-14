package main

import (
	"fmt"
	"io/ioutil"
	"time"
	"strings"
	"strconv"
	"os/exec"
)

func getDiskInfo() {

}

func getMemoryValue(memType string) string {
	var memorySize []string
	var memorySizeValue string

	// Read "/proc/meminfo" file
	meminfoFile, err := ioutil.ReadFile("/proc/meminfo")
	meminfo := string(meminfoFile)
	if err != nil {
		fmt.Println(err)
	}
	lines := strings.Split(meminfo, "\n")
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


func unit(value string) string {
    /** Function to convert value to human-readable format */

	intValue, _ := strconv.Atoi(value)
	length := len(value)

	if length > 6 {
		gb := float64(intValue) / (1024 * 1024)
		roundedValue := fmt.Sprintf("%.2f", gb)
		return roundedValue + " GB"
	} else if length >= 4 && length <= 6 {
		mb := float64(intValue) / 1024
		roundedValue := fmt.Sprintf("%.2f", mb)
		return roundedValue + " MB"
	} else {
		roundedValue := fmt.Sprintf("%.2f", float64(intValue))
		return roundedValue + " KB"
	}
}


func getMemoryInfo() {

	//total:=getMemoryValue("MemTotal")
	freeStr:=getMemoryValue("MemFree")
	buffersStr:=getMemoryValue("Buffers")
	availableStr:=getMemoryValue("MemTotal")
	cachedStr:=getMemoryValue("Cached")
	KReclaimableStr:=getMemoryValue("KReclaimable")
	hugepagesizeStr:=getMemoryValue("Hugepagesize")

	//memTotal, err := strconv.Atoi(total)
	freeInt, err := strconv.Atoi(freeStr)
	buffersInt, err := strconv.Atoi(buffersStr)
	availableInt, err := strconv.Atoi(availableStr)
	cachedInt, err := strconv.Atoi(cachedStr)
	KReclaimableInt, err := strconv.Atoi(KReclaimableStr)
	hugepagesizeInt, err := strconv.Atoi(hugepagesizeStr)

	if(err != nil) {
		fmt.Println(err)
	}

	fmt.Println("memAvailable "+availableStr)
	fmt.Println("memFree "+freeStr)
	fmt.Println("buffers "+buffersStr)
	fmt.Println("cached "+cachedStr)
	fmt.Println("KReclaimable "+KReclaimableStr)
	fmt.Println("hugepagesize "+hugepagesizeStr)
	//fmt.Println("memTotal "+totalStr)

	// Calculate mem_used
	usedInt := availableInt - freeInt - buffersInt - cachedInt - KReclaimableInt - hugepagesizeInt

	// Calculate percentage
	percentage := (usedInt * 100) / availableInt
	
	// Convert values to human-readable format
	usedHuman := unit(strconv.Itoa(usedInt))
	availableHuman := unit(availableStr)

	fmt.Println(usedInt)
	fmt.Println(percentage)
	fmt.Println(usedHuman)
	fmt.Println(availableHuman)

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
func getCPUInfo() {
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
		return
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

	fmt.Println(cpuUsageArray)
	
}


func runSockerServer(){}


func main() {
	//getCPUInfo()
	getMemoryInfo()
}
