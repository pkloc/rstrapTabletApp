import tkinter as tk
from serial.tools import list_ports
import serial as serial

class MainApplication(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        master.title("Phil's App")

        self.device_port = ""
        self.baud_rate = 9600
        self.serial = serial.Serial()
        self.serial_input = ''

        self.button = tk.Button(master, text="Find device", command=self.find_device)
        self.button.pack()

        # make a scrollbar
        self.scrollbar = tk.Scrollbar(master)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        # make a text box to put the serial output
        self.log = tk.Text(master, width=30, height=30, takefocus=0)
        self.log.pack()

        # attach text box to scrollbar
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command = self.log.yview)

    def find_device(self):
        for port_info in list_ports.comports():
            if 'Arduino' in port_info.description:
                print('found device: ' + port_info.description)
                self.device_port = port_info.device
                self.serial = serial.Serial(self.device_port, self.baud_rate, timeout=0)
                self.readSerial()

    def readSerial(self):
        try:            
            if self.serial.is_open:
                self.serial_input = self.serial_input + self.serial.readline().decode('utf-8')

                if self.serial_input.endswith('\n'):
                    self.log.insert('0.0', self.serial_input)
                    self.serial_input = ''
            else:
                self.serial = serial.Serial(self.device_port, self.baud_rate, timeout=0)

        except:
            print('No data')

            if self.serial.is_open:
                self.serial.close()

        self.master.after(100, self.readSerial)

        
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

