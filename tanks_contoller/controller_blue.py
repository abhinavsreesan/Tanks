import pygame
from pygame.locals import *
import socket
import sys, getopt
from Tkinter import *

class Controller:

    DEFAULT_PORT = 1111

    def __init__(self, ip):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1100, 500
        self._host = ip
        self._port = self.DEFAULT_PORT

    def _netcat(self, content):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(content, (self._host, self._port))

    def on_init(self):
        pygame.init()
        pygame.font.init()

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.render_nes()

        pygame.display.update()

    def on_event(self, event):

        key = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pygame.draw.polygon(self._display_surf, (220,220,220), [[215, 160], [245, 190],[230,190],[230,230],[200,230],[200,190],[185,190]])
                self._netcat(b"\x01")
            if event.key == pygame.K_d:
                pygame.draw.polygon(self._display_surf, (220,220,220), [[340, 285], [310, 315],[310,300],[270,300],[270,270],[310,270],[310,255]])
                self._netcat(b"\x05")
            if event.key == pygame.K_s:
                pygame.draw.polygon(self._display_surf, (220,220,220), [[215, 405], [185, 375],[200,375],[200,335],[230,335],[230,375],[245,375]])
                self._netcat(b"\x03")
            if event.key == pygame.K_a:
                pygame.draw.polygon(self._display_surf, (220,220,220), [[87, 285], [117, 255],[117,270],[157,270],[157,300],[117,300],[117,315]])
                self._netcat(b"\x07")
            if event.key == pygame.K_k:
                pygame.draw.circle(self._display_surf, (176,224,230), [770, 360], 50)
                self._netcat(b"\x09")
            if event.key == pygame.K_l:
                pygame.draw.circle(self._display_surf, (176,224,230), [930, 360], 50)
                self._netcat(b"\x09")
            if event.key == pygame.K_i:
                pygame.draw.rect(self._display_surf, (220,220,220), (422,367,76,26))
                self.render_legend()
            if event.key == pygame.K_o:
                pygame.draw.rect(self._display_surf, (220,220,220), (582,367,76,26))
                self.render_legend()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                pygame.draw.polygon(self._display_surf, (0,0,0), [[215, 160], [245, 190],[230,190],[230,230],[200,230],[200,190],[185,190]])
                pygame.draw.polygon(self._display_surf, (128,128,128), [[215, 160], [245, 190],[230,190],[230,230],[200,230],[200,190],[185,190]], 2)
                self._netcat(b"\x02")
            if event.key == pygame.K_d:
                pygame.draw.polygon(self._display_surf, (0,0,0), [[340, 285], [310, 315],[310,300],[270,300],[270,270],[310,270],[310,255]])
                pygame.draw.polygon(self._display_surf, (128,128,128), [[340, 285], [310, 315],[310,300],[270,300],[270,270],[310,270],[310,255]], 2)
                self._netcat(b"\x06")
            if event.key == pygame.K_s:
                pygame.draw.polygon(self._display_surf, (0,0,0), [[215, 405], [185, 375],[200,375],[200,335],[230,335],[230,375],[245,375]])
                pygame.draw.polygon(self._display_surf, (128,128,128), [[215, 405], [185, 375],[200,375],[200,335],[230,335],[230,375],[245,375]], 2)
                self._netcat(b"\x04")
            if event.key == pygame.K_a:
                pygame.draw.polygon(self._display_surf, (0,0,0), [[87, 285], [117, 255],[117,270],[157,270],[157,300],[117,300],[117,315]])
                pygame.draw.polygon(self._display_surf, (128,128,128), [[87, 287], [117, 255],[117,270],[157,270],[157,300],[117,300],[117,315]], 2)
                self._netcat(b"\x08")
            if event.key == pygame.K_k:
                pygame.draw.circle(self._display_surf, (0,0,255), [770, 360], 50)
                self._netcat(b"\x00")
            if event.key == pygame.K_l:
                pygame.draw.circle(self._display_surf, (0,0,255), [930, 360], 50)
                self._netcat(b"\x00")
            if event.key == pygame.K_i:
                pygame.draw.rect(self._display_surf, (0,0,0), (422,367,76,26))
                self.render_nes()
            if event.key == pygame.K_o:
                pygame.draw.rect(self._display_surf, (0,0,0), (582,367,76,26))
                self.render_nes()

        pygame.display.update()

    def on_loop(self):
        pass

    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def render_nes(self):

        pygame.display.set_caption("Tanks Controller")
        # fill display surf with color grey
        self._display_surf.fill((220,220,220))

        # black rectangle serving as base
        pygame.draw.rect(self._display_surf, (0,0,0), (50,100,1000,370))

        # red round button in grey squares
        pygame.draw.rect(self._display_surf, (220,220,220), (870,300,120,120))
        pygame.draw.rect(self._display_surf, (220,220,220), (710,300,120,120))
        pygame.draw.circle(self._display_surf, (0,0,255), [770, 360], 50)
        pygame.draw.circle(self._display_surf, (0,0,255), [930, 360], 50)

        # grey colored midribs
        pygame.draw.rect(self._display_surf, (220,220,220), (390,300,300,120)) # main mid rib with buttons
        pygame.draw.rect(self._display_surf, (220,220,220), (390,100,300,60))
        pygame.draw.rect(self._display_surf, (220,220,220), (390,180,300,100))
        pygame.draw.rect(self._display_surf, (220,220,220), (390,440,300,30))

        # gray color base for arrow keys
        pygame.draw.rect(self._display_surf, (220,220,220), (170,150,90,90))
        pygame.draw.rect(self._display_surf, (220,220,220), (80,240,90,90))
        pygame.draw.rect(self._display_surf, (220,220,220), (260,240,90,90))
        pygame.draw.rect(self._display_surf, (220,220,220), (170,330,90,90))
        pygame.draw.rect(self._display_surf, (220,220,220), (170,240,90,90))

        # black colored center fill for arrow keys
        pygame.draw.line(self._display_surf, (0,0,0), (390,100), (690,100), 2)
        pygame.draw.line(self._display_surf, (0,0,0), (390,468), (690,468), 2)

        # black colored arrow keys
        pygame.draw.rect(self._display_surf, (0,0,0), (172,152,86,86))
        pygame.draw.rect(self._display_surf, (0,0,0), (82,242,86,86))
        pygame.draw.rect(self._display_surf, (0,0,0), (262,242,86,86))
        pygame.draw.rect(self._display_surf, (0,0,0), (172,332,86,86))
        pygame.draw.rect(self._display_surf, (0,0,0), (168,242,94,86))
        pygame.draw.rect(self._display_surf, (0,0,0), (172,238,86,94))

        # grey colored directional arrows on arrow key
        pygame.draw.polygon(self._display_surf, (128,128,128), [[215, 160], [245, 190],[230,190],[230,230],[200,230],[200,190],[185,190]], 2)
        pygame.draw.polygon(self._display_surf, (128,128,128), [[340, 285], [310, 315],[310,300],[270,300],[270,270],[310,270],[310,255]], 2)
        pygame.draw.polygon(self._display_surf, (128,128,128), [[215, 405], [185, 375],[200,375],[200,335],[230,335],[230,375],[245,375]], 2)
        pygame.draw.polygon(self._display_surf, (128,128,128), [[87, 285], [117, 255],[117,270],[157,270],[157,300],[117,300],[117,315]], 2)
        # grey circle in the center of the arrow key
        pygame.draw.circle(self._display_surf, (128,128,128), [215, 285], 30, 2)

        # start and select black buttons
        pygame.draw.rect(self._display_surf, (0,0,0), (420,365,80,30))
        pygame.draw.rect(self._display_surf, (0,0,0), (580,365,80,30))

        # all the test on the screen
        ninfont = pygame.font.SysFont('Arial', 50)
        rfont = pygame.font.SysFont('Arial', 15)
        Afont = pygame.font.SysFont('Arial', 40)
        startfont = pygame.font.SysFont('Arial', 25)
        textsurface = ninfont.render('Tanks V1.0', False, (0,0,255))
        self._display_surf.blit(textsurface,(430,210))
        pygame.draw.circle(self._display_surf, (0,0,255), [653, 220], 10, 2)
        rtextsurface = rfont.render('R', False, (0,0,255))
        self._display_surf.blit(rtextsurface,(650,211))
        atextsurface = Afont.render('A', False, (0,0,255))
        self._display_surf.blit(atextsurface,(970,418))
        btextsurface = Afont.render('B', False, (0,0,255))
        self._display_surf.blit(btextsurface,(810,418))
        starttextsurface = startfont.render('START', False, (0,0,255))
        self._display_surf.blit(starttextsurface,(428,330))
        selecttextsurface = startfont.render('SELECT', False, (0,0,255))
        self._display_surf.blit(selecttextsurface,(583,330))

        # technical team logo
        tech_logo_img = pygame.image.load('techlogo.png')
        self._display_surf.blit(tech_logo_img, (840,100))


    def render_legend(self):
        pygame.draw.rect(self._display_surf, (255,255,255), (250,50,600,300))
        legendfont = pygame.font.SysFont('Comic Sans MS', 20)
        wtextsurface = legendfont.render('W = Forward', False, (0,0,255))
        self._display_surf.blit(wtextsurface, (280,70))
        atextsurface = legendfont.render('A = Left', False, (0,0,255))
        self._display_surf.blit(atextsurface, (280,100))
        stextsurface = legendfont.render('S = Backward', False, (0,0,255))
        self._display_surf.blit(stextsurface, (280,130))
        dtextsurface = legendfont.render('D = Right', False, (0,0,255))
        self._display_surf.blit(dtextsurface, (280,160))
        ftextsurface = legendfont.render('K / B on Nes = Shoot', False, (0,0,255))
        self._display_surf.blit(ftextsurface, (280,190))
        gtextsurface = legendfont.render('L / A on Nes = Shoot', False, (0,0,255))
        self._display_surf.blit(gtextsurface, (280,220))
        etextsurface = legendfont.render('I / Select on Nes = Legend (Hold)', False, (0,0,255))
        self._display_surf.blit(etextsurface, (280,250))
        rtextsurface = legendfont.render('O / Start on Nes = Legend (Hold)', False, (0,0,255))
        self._display_surf.blit(rtextsurface, (280,280))

def connect(ipEntry):
    ipAddressEntered = str(ipEntry.get())
    nes = Controller(ipAddressEntered)
    nes.on_execute()

def main():

    rootWindow = Tk()
    rootWindow.title("Tanks Controller - Blue")
    # rootWindow.geometry((500,300))
    rootWindow.geometry(("%dx%d")%(475,100))
    welcomeLabel = Label(
                        rootWindow,
                        text = "Tanks Controller v1.0",
                        fg = "blue",
                        font = "Helvetica 16 bold"
                   )
    welcomeLabel.grid(row=0, columnspan=2, sticky=W+E+S+N)
    ipLabel = Label(
                        rootWindow,
                        text = "Enter the IP address of your tank:  ",
                        fg = "blue",
                        font = "Helvetica 14 bold"
                   )
    ipLabel.grid(row=1, column=0)
    ipEntry  = Entry(rootWindow)
    ipEntry.grid(row=1, column=1)

    buttonConnect = Button(
                        rootWindow,
                        text = "Connect",
                        command = lambda: connect(ipEntry)
                    )
    buttonQuit = Button(
                    rootWindow,
                    text = "Quit",
                    command = rootWindow.quit
                )
    buttonConnect.grid(row=2, column=0)
    buttonQuit.grid(row=2, column=1)


    rootWindow.mainloop()

if __name__ == "__main__" :

    main()
