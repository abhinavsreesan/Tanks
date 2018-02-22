import pygame
import socket
import sys,getopt


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
                        print "Forward"
                        self._netcat(b"\x01")
                    if event.key == pygame.K_a:
                        print "Left"
                        self._netcat(b"\x07")
                    if event.key == pygame.K_s:
                        print "Backward"
                        self._netcat(b"\x03")
                    if event.key == pygame.K_d:
                        print "Right"
                        self._netcat(b"\x05")
                    if event.key == pygame.K_ESCAPE:
                        break

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        print "Forward released"
                        self._netcat(b"\x02")
                    if event.key == pygame.K_a:
                        print "Left released"
                        self._netcat(b"\x08")
                    if event.key == pygame.K_s:
                        print "Backward released"
                        self._netcat(b"\x04")
                    if event.key == pygame.K_d:
                        print "Right released"
                        self._netcat(b"\x06")


            pygame.display.update()
        pygame.quit

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:", ["host="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    host = ""
    for o, a in opts:
        if o in ("-h", "--host"):
            host = a

    if host == "":
        print("Did not define host, use -h or --host to pass the host name of the car")
        sys.exit(2)

    p = Controller(host)
    p.start()
def usage():
    print("Available options:")
    print("-h, --host  Define RC car IP address")


if __name__ == "__main__":
    main()
