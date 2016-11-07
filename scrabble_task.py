#! /usr/bin/env python

import pygame
import string

# Constants
color_font = (30, 30, 30)
background_color = (255, 255, 255)
box_edge_color = (0, 0, 0)
box_back_color = (240, 240, 240)
box_text_color = (100, 100, 100)
button_edge_color = (0, 0, 0)
button_back_color = (200, 200, 200)
button_text_color = (40, 40, 40)
box_width = 250
box_height = 60
button_width = 150
button_height = 35
screen_w = 640
screen_h = 500
fps = 60
screen = pygame.display.set_mode((screen_w, screen_h))
wait_time = 1000


def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        elif event.type == pygame.MOUSEBUTTONUP:
            return event.pos
        else:
            pass


class Stimulus:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 60)

    def draw_letterset(self, letters):
        self.surface.fill(background_color)
        text = self.font.render(letters, 1, color_font)
        screen.blit(text, (self.x - 115, self.y - 150))


class Input:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.current_string = []
        self.previous_string = ""
        self.font = pygame.font.Font(None, 50)

    def draw_text_box(self, message):
        # Draw text box
        pygame.draw.rect(self.surface, box_back_color,
                         ((self.x - (box_width / 2)), self.y,
                          box_width, box_height), 0)
        pygame.draw.rect(self.surface, box_edge_color,
                         ((self.x - (box_width / 2)), self.y,
                          box_width, box_height), 1)

        if len(message) != 0:
            self.surface.blit(self.font.render(message, 1, box_text_color),
                              (self.x - 100, self.y + 10))

        pygame.display.flip()

    def draw_input(self):
        # Draw user input
        self.draw_text_box(string.join(self.current_string, ""))
        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.current_string = self.current_string[:-1]
                elif event.key == pygame.K_RETURN:
                    self.previous_string = self.current_string
                    self.current_string = []
                    # check whether self.previous_string is a correct word
                    # If yes: save as correct, if no: save as incorrect
                    print string.join(self.previous_string, "")
                elif event.key <= 127:
                    self.current_string.append(chr(event.key))
            elif event.type == pygame.MOUSEBUTTONUP:
                print "You released at (%d, %d)" % event.pos
                if self.x - (button_width / 2) <= event.pos[0] <= \
                             self.x + (button_width / 2) and \
                    self.y + 100 <= event.pos[1] <= self.y + 100 + \
                                button_height:
                    break

            self.draw_text_box(string.join(self.current_string, ""))


class Checker:
    def __init__(self, stimulus, cor_words):
        self.correct = cor_words
        self.stimulus = stimulus


class Wait:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 30)

    def intro(self, message):
        self.surface.fill(background_color)
        text = self.font.render(message, 1, color_font)
        self.surface.blit(text, (self.x - 115, self.y))
        pygame.display.flip()
        while True:
            inkey = get_key()
            print inkey
            if inkey == pygame.K_SPACE:
                return

    def waiter(self):
        self.surface.fill(background_color)
        text = self.font.render("Wacht op de volgende letterset", 1,
                                color_font)
        self.surface.blit(text, (self.x - 115, self.y))
        pygame.display.flip()
        pygame.time.delay(wait_time)
        self.surface.fill(background_color)


class Button:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 30)

    def next_set(self):
        pygame.draw.rect(self.surface, button_back_color,
                         ((self.x - (button_width / 2)), self.y + 100,
                          button_width, button_height), 0)
        pygame.draw.rect(self.surface, button_edge_color,
                         ((self.x - (button_width / 2)), self.y + 100,
                          button_width, button_height), 1)
        text = self.font.render("volgende set", 1, color_font)
        screen.blit(text, (self.x - button_width / 2 + 12, self.y + 105))
        pygame.display.flip()


def main():
    stimulus_set = ["I E N T W R", "A N T G E S"]
    # correct_words = [["winter", "niet", "nier", "trein"],
    #                  ["agent", "agens", "tang", "stang"]]

    # Initialize
    pygame.init()
    screen.fill(background_color)

    # Initiate objects
    stimulus = Stimulus(screen)
    user_input = Input(screen)
    wait = Wait(screen)
    button = Button(screen)

    wait.intro("Welkom, druk op spatie om verder te gaan")

    for word in stimulus_set:
        begin = pygame.time.get_ticks()
        stimulus.draw_letterset(word)
        button.next_set()
        user_input.draw_input()
        end = pygame.time.get_ticks()
        time = end - begin
        print "Time spent in set: ", time / 1000, " seconds."
        wait.waiter()

    screen.fill(background_color)

if __name__ == '__main__':
    main()

"""-------------------DUMP-------------------"""
# clock = pygame.time.Clock()
# clock.tick(fps)
# print text.previous_string

# if event.type == pygame.QUIT:
#     running = False
# elif event.type == pygame.KEYDOWN:
#     if event.key == pygame.K_ESCAPE:
#         running = False
# else:
#     pass

# running = True

# check whether word is in correct words
# http://stackoverflow.com/questions/17687379/python-check-for-word-in-list
# http://stackoverflow.com/questions/20175286/python-check-if-word-matches-list-of-words-with-if-statement
# some_list = ['abc-123', 'def-456', 'ghi-789', 'abc-456']
# if any("abc" in s for s in some_list):
#     # whatever
