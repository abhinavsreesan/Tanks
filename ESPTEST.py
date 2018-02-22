import pygame
import socket
import sys,getopt
from Tkinter import *

class Controller:
    DEFAULT_PORT = 1111

    def __init__(self, ip):
        self._create_ui()
        self._host = ip
        self._port = self.DEFAULT_PORT

    def _netcat(self, content):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(content, (self._host, self._port))

    def start(self):
    	self._loop()
    def _create_ui(self):
    	screen = pygame.display.set_mode([300,100])
    	screen.fill([255,255,255])
    	pygame.display.set_caption("Windows Controller")


    def _loop(self):
        while 1:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        print "Forward Right"
                        self._netcat(b"\x01")
                    if event.key == pygame.K_q:
                        print "Forward Left"
                        self._netcat(b"\x07")
                    if event.key == pygame.K_a:
                        print "Backward Left"
                        self._netcat(b"\x03")
                    if event.key == pygame.K_s:
                        print "Backwards Right"
                        self._netcat(b"\x05")
                    if event.key == pygame.K_f:
                        print "Trigger Armed"
                        self._netcat(b"\x09")
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        print "Forward RIght released"
                        self._netcat(b"\x02")
                    if event.key == pygame.K_q:
                        print "Forward Left released"
                        self._netcat(b"\x08")
                    if event.key == pygame.K_a:
                        print "Backward Left released"
                        self._netcat(b"\x04")
                    if event.key == pygame.K_s:
                        print "Backwards Right released"
                        self._netcat(b"\x06")
                    if event.key == pygame.K_f:
                        print "Trigger released"
                        self._netcat(b"\x00")

            pygame.display.update()
        pygame.quit

def connect(ipValueOne, ipValueTwo, ipValueThree, ipValueFour):
    ipAddressEntered = str(ipValueOne.get())
    ipAddressEntered = ipAddressEntered + "." + str(ipValueTwo.get()) + "." + str(ipValueThree.get()) + "." + str(ipValueFour.get())
    p = Controller(ipAddressEntered)
    p.start()

def main():
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "h:", ["host="])
    # except getopt.GetoptError as err:
    #     print(str(err))
    #     usage()
    #     sys.exit(2)
    # host = ""
    # for o, a in opts:
    #     if o in ("-h", "--host"):
    #         host = a
    #
    # if host == "":
    #     print("Did not define host, use -h or --host to pass the host name of the car")
    #     sys.exit(2)

    rootWindow = Tk()
    welcomeLabel = Label(
                        rootWindow,
                        text = "Tanks Controller v1.0",
                        fg = "Blue",
                        font = "Ariel 16 bold"
                   )
    welcomeLabel.grid(row=0, column=0, columnspan=7, sticky=W+E+S+N)
    
    ipLabel = Label(
                        rootWindow,
                        text = "Enter the IP address of your tank:  ",
                        fg = "red",
                        font = "Helvetica 14 bold"
                   )
    ipLabel.grid(row=1, column=0, columnspan=7, sticky=W+E+S+N)

        
    def limitIPSizeOne(*args):
        value = ipValueOne.get()
        if(len(value)) >= 3: 
            ipValueOne.set(value[:3])
            ipEntry2.focus()
            
    def limitIPSizeTwo(*args):
        value = ipValueTwo.get()
        if(len(value)) >= 3: 
            ipValueTwo.set(value[:3])
            ipEntry3.focus()
            
    def limitIPSizeThree(*args):
        value = ipValueThree.get()
        if(len(value)) >= 3: 
            ipValueThree.set(value[:3])
            ipEntry4.focus()
    
    def limitIPSizeFour(*args):
        value = ipValueFour.get()
        if(len(value)) >= 3: 
            ipValueFour.set(value[:3])
            
        
    ipValueOne = StringVar()
    ipValueOne.trace('w', limitIPSizeOne)
    
    ipValueTwo = StringVar()
    ipValueTwo.trace('w', limitIPSizeTwo)
    
    ipValueThree = StringVar()
    ipValueThree.trace('w', limitIPSizeThree)
    
    ipValueFour = StringVar()
    ipValueFour.trace('w', limitIPSizeFour)
    
    ipEntry1  = Entry(rootWindow, width=5, textvariable=ipValueOne)
    ipEntry2  = Entry(rootWindow, width=5, textvariable=ipValueTwo)
    ipEntry3  = Entry(rootWindow, width=5, textvariable=ipValueThree)
    ipEntry4  = Entry(rootWindow, width=5, textvariable=ipValueFour)
    dotLabel1 = Label(rootWindow, text=".")
    dotLabel2 = Label(rootWindow, text=".")
    dotLabel3 = Label(rootWindow, text=".")
    ipEntry1.grid(row=2, column=0)
    dotLabel1.grid(row=2, column=1)
    ipEntry2.grid(row=2, column=2)
    dotLabel2.grid(row=2, column=3)
    ipEntry3.grid(row=2, column=4)
    dotLabel3.grid(row=2, column=5)
    ipEntry4.grid(row=2, column=6)
        
    buttonConnect = Button(
                        rootWindow,
                        text = "Connect",
                        command = lambda: connect(ipValueOne, ipValueTwo, ipValueThree, ipValueFour)
                    )
    buttonQuit = Button(
                    rootWindow,
                    text = "Quit",
                    command = rootWindow.quit
                )
    buttonConnect.grid(row=3, column=1, columnspan=2)
    buttonQuit.grid(row=3, column=4, columnspan=2)


    rootWindow.mainloop()
    # p = Controller(host)
    # p.start()

def usage():
    print("Available options:")
    print("-h, --host  Define RC car IP address")


if __name__ == "__main__":
    main()
