# Python utilities
import time, threading, curses

# TLK imports
from tlk.utilities.hypervisor import Hypervisor


class RealTimeScreen:

    def __init__(self):
        self.exit_flag = threading.Event()  #Event to signal the end of the cycle
        self.qubik = Hypervisor()
    #End_def


    def monitor_server(self, window):
        ''' '''

        while not self.exit_flag.is_set():
            # Get CPU values
            window.addstr(0, 0, "===CPU===\n")
            cpu_values = self.getCPUValues()

            # Clear the CPU values line
            window.move(1, 0)
            window.clrtoeol()

            # Print CPU values in a single line
            cpu_line = " ".join([f"{cpu}: {valor}%     " for cpu, valor in cpu_values.items()])
            window.addstr(1, 0, cpu_line)

            # Print memory values
            memory_values = self.getMemoryValues()
            memory_line = f"Used: {memory_values['used']} of {memory_values['available']} [{memory_values['percentage']}%]"
            
            window.addstr(2, 0, "===Memory===")
            window.addstr(3, 0, memory_line)

            # Refresh the window
            window.refresh()

            # Wait for a time interval before the next update
            time.sleep(1)

        window.addstr("\nExiting...")
        window.refresh()
    #End_def


    def getCPUValues(self):
        ''' Get CPU values from hypervisor module '''
        cpu_values = self.qubik.cpu.read()
        
        return cpu_values
    #End_def


    def getMemoryValues(self):
        ''' Get Memory values from hypervisor module '''
        memory_values = self.qubik.memory.read()

        return memory_values
    #End_def


    def getDiskValues(self, stdscr):
        ''' '''
        disk_values = self.qubik.disk.read()
        disk_line = f"Used: {disk_values['used']} of {disk_values['available']} [{disk_values['percentage']}]"
        stdscr.addstr(4, 0, "===Disk===")
        stdscr.addstr(5, 0, disk_line)
        stdscr.refresh()
    #End_def


    def askForOutput(self, stdscr):
        ''' '''
        stdscr.addstr(6, 0, "\nPress ENTER to exit!", curses.A_BOLD)  # Add the A_BOLD atrribute for bold text
        stdscr.refresh()
        while True:
            option = stdscr.getch()
            if option == ord('\n'):  # Chek if Enter key was pressed
                self.exit_flag.set()  # Set the output signal
                break
    #End_def


    def screen(self, stdscr):
        ''' '''
        curses.curs_set(0)  # Hide the cursor

        # Create and execute the threads
        monitor_thread   = threading.Thread(target=self.monitor_server, args=(stdscr,))
        disk_thread      = threading.Thread(target=self.getDiskValues, args=(stdscr,))
        ask_thread = threading.Thread(target=self.askForOutput, args=(stdscr,))

        monitor_thread.start()
        disk_thread.start()
        ask_thread.start()

        # Wait for both threads to finish
        monitor_thread.join()
        disk_thread.join()
        ask_thread.join()
    #End_def


    def cursesWrapper(self):
        ''' '''
        rts = RealTimeScreen()
        curses.wrapper(rts.screen)
    #End_def
