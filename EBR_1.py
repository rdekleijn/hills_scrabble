#! /usr/bin/env python

import pygame
import cv2
import os
import sys
import random
from timeit import default_timer as timer

# Constants
color_font = (30, 30, 30)
background_color = (255, 255, 255)
screen_w = 640
screen_h = 500
fps = 60
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE |
                                 pygame.DOUBLEBUF | pygame.FULLSCREEN)
ebr_time = 360.0


class Stimulus:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 20)
        self.font_cross = pygame.font.Font(None, 300)

    def intro(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images",
                                               "EBR_intro_1.jpg")).convert()
        self.surface.blit(image, (50, 50))
        pygame.display.flip()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

    def outro(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images",
                                               "EBR_outro_1.jpg")).convert()
        self.surface.blit(image, (50, 50))
        pygame.display.flip()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

    def draw_fixation(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images", "fixation.jpg")).convert()
        self.surface.blit(image, (50, 50))
        pygame.display.flip()


class Main:
    def __init__(self, subjectID, condition):
        self.subjectID = subjectID
        self.condition = condition
        filename = str(self.subjectID) + "_EBR_1" + ".txt"
        f = open(filename, 'w')
        output = 'subjectID,condition,time_start,time_end\n'
        f.write(output)
        f.close()

        # Init task
        pygame.init()
        pygame.mouse.set_visible(False)
        self.surface = screen
        self.surface.fill(background_color)
        self.running = True
        self.start = 0

        # Initiate objects
        self.stimulus = Stimulus(screen)

    def main(self):
        # Main loop
        clock = pygame.time.Clock()
        self.stimulus.intro()
        self.stimulus.draw_fixation()

        cap = cv2.VideoCapture(0)

        # Define the codec and create VideoWriter object
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter(str(self.subjectID) + '_EBR1.avi', fourcc, 20.0, (640, 480))

        self.start = timer()

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                out.write(frame)
                cv2.imshow('frame', frame)
                if timer() - self.start > ebr_time:
                    self.running = False

                if self.running == False:
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        self.stimulus.outro()
        self.end = timer()

        clock.tick(60)

        filename = str(self.subjectID) + "_EBR_1" + ".txt"
        f = open(filename, 'a')
        output = str(self.subjectID) + "," + \
                 self.condition + "," + \
                 str(self.start) + "," + \
                 str(self.end) + "\n"
        f.write(output)
        f.close()

if __name__ == '__main__':
    subject_ID = sys.argv[1]
    if sys.argv[2] == "r":
        condition = random.choice(("c", "d"))
    else:
        condition = sys.argv[2]
    run = Main(subject_ID, condition)
    run.main()
