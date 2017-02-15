import tkinter as tk
from tkinter import messagebox
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

        self.connect_button = tk.Button(master, text="Connect to device", command=self.connect_to_device, height=4, width=20)        
        self.connect_button.pack()

        # make a scrollbar
        self.scrollbar = tk.Scrollbar(master)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        # make a text box to put the serial output
        self.log = tk.Text(master, width=30, height=30, takefocus=0)
        self.log.pack()

        # attach text box to scrollbar
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command = self.log.yview)

    def connect_to_device(self):
        device_found = False

        for port_info in list_ports.comports():
            print('found device: ' + port_info.description)
            if 'Arduino' in port_info.description:
                device_found = True
                self.connect_button.config(state = 'disabled')
                print('connecting to device: ' + port_info.description)
                self.device_port = port_info.device
                self.serial = serial.Serial(self.device_port, self.baud_rate, timeout=0)
                self.readSerial()
            

        if not device_found:
            messagebox.showinfo('Device not found', 'No devices have been found')

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

