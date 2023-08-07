import time, subprocess


class CPU:
    ''' '''

    def get_cores(self):
        ''' '''
        proc0 = subprocess.Popen(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE)
        proc1 = subprocess.Popen(["grep", "processor"], stdin=proc0.stdout, stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(["wc", "-l"], stdin=proc1.stdout, stdout=subprocess.PIPE)
        numbers, error = proc2.communicate()
        cores = int(numbers.decode('utf-8'))

        return cores
    ## END def


    def read_cpu_times(self):
        ''' '''
        all_cpu = {}
        cores = self.get_cores()
        for number in range(cores):
            cpun = 'cpu'+str(number)
            proc00 = subprocess.Popen(["more", "/proc/stat"], stdout=subprocess.PIPE)
            proc02 = subprocess.Popen(["grep", cpun], stdin=proc00.stdout, stdout=subprocess.PIPE)
            output, error = proc02.communicate()
            cpu_times = output.decode('utf-8')
            all_cpu[cpun] = [int(i) for i in cpu_times.split()[1:]]

        return all_cpu
    ## END def


    def read(self):
        ''' '''

        ## Getting CPU times
        cpu_times1 = self.read_cpu_times()
        time.sleep(0.5)
        cpu_times2 = self.read_cpu_times()

        cpu_name_list = list(cpu_times1.keys())
        cpu_percentages = {}


        for cpu_name in cpu_name_list:

            # CPU time structures
            cpu_array_times1 = cpu_times1[cpu_name]
            cpu_array_times2 = cpu_times2[cpu_name]

            # CPU delta times
            delta_idle_cpu = cpu_array_times2[3] - cpu_array_times1[3]
            delta_system_cpu = cpu_array_times2[2] - cpu_array_times1[2]
            cpu_total_time = (delta_system_cpu) + (delta_idle_cpu)

            # CPU percentage
            percentage = (1 - (delta_idle_cpu / cpu_total_time)) * 100
            cpu_percentages[cpu_name] = round(percentage, 2)
        ## END for


        ## CPU Percentage %
        return cpu_percentages
    #End_def

##End_Class


class Memory:
    ''' '''

    def read(self):
        ''' '''
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
    
        # Memory Values
        mem_available = lines[0].split()[1]
        mem_available = int(mem_available)

        mem_free = lines[1].split()[1]
        mem_free = int(mem_free)

        buffers = 0
        cached = 0
        kreclaimable = 0
        huge_page_size = 0
        file_system_mem = 0

        for line in lines:
            if line.startswith('Buffers:'):
                buffers = line.split()[1]
                buffers = int(buffers)

            elif line.startswith('Cached:'):
                cached = line.split()[1]
                cached = int(cached)

            elif line.startswith('KReclaimable:'):
                kr = line.split()[1]
                kr = int(kr)

            elif line.startswith('Hugepagesize:'):
                huge_page_size = line.split()[1]
                huge_page_size = int(huge_page_size)
        #End_for

        mem_used = round(mem_available - mem_free - buffers - cached - kr - huge_page_size, 2)

        percentage = round( (mem_used / mem_available) * 100, 2 )

        return {
            'used': self.unit(mem_used), 
            'available': self.unit(mem_available), 
            'percentage': percentage
        }
    #End_def


    def unit(self, value):
        ''' '''
        integer = int(value)

        if( 6 < len(str(integer)) ):
            gb = float(value) / 1024**2
            rounded_value = round(gb, 2)
            value = f"{rounded_value} GB"

        elif( 6 >= len(str(integer)) >= 4 ):
            mb = float(value) / 1024
            rounded_value = round(mb, 2)
            value = f"{rounded_value} MB"

        elif( 4 > len(str(integer)) >= 1 ):
            rounded_value = round(value, 2)
            value = f"value {rounded_value} KB"

        return value
    #End_def

## END_Class


class Disk:
    ''' '''

    def read(self):
        ''' '''
        output = subprocess.check_output(['df', '/','-h']).decode('utf-8')
        lines = output.split('\n')
        values = lines[1].split()

        return {
            'used': values[2],
            'available': values[1],
            'percentage': values[4]
        }
        #print(f' Used: {values[2]} of {values[1]}  [{values[4]}]')
    #End_def

#End_Class