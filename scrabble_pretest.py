#! /usr/bin/env python

import pygame
import string
import csv
import os
import sys
import random
from timeit import default_timer as timer

# Constants
color_font = (30, 30, 30)
background_color = (255, 255, 255)
box_edge_color = (0, 0, 0)
box_back_color = (240, 240, 240)
box_text_color = (100, 100, 100)
button_edge_color = (0, 0, 0)
button_back_color = (200, 200, 200)
button_text_color = (40, 40, 40)
incorrect_color = (255, 0, 40)
correct_color = (50, 255, 0)
counter_text_color = (150, 150, 150)
box_width = 250
box_height = 60
button_width = 150
button_height = 35
screen_w = 640
screen_h = 500
fps = 60
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE |
                                 pygame.DOUBLEBUF | pygame.FULLSCREEN)
wait_time = 15000


class Stimulus:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 60)

    def draw_letterset(self, letters):
        self.surface.fill(background_color)
        text = self.font.render(letters, 1, color_font)
        self.surface.blit(text, (self.x - 110, self.y - 150))


class Input:
    """This class takes care of user input"""
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.current_string = []
        self.previous_string = ""
        self.past_correct_words = []
        self.past_incorrect_words = []
        self.n_correct_words = 0
        self.n_incorrect_words = 0
        self.prev_n_correct = 0
        self.prev_n_incorrect = 0
        self.total_correct_words = 0
        self.total_incorrect_words = 0
        self.font = pygame.font.Font(None, 50)
        self.font_feedback = pygame.font.Font(None, 40)
        self.font_counter = pygame.font.Font(None, 25)

    def draw_text_box(self, message):
        pygame.draw.rect(self.surface, box_back_color,
                         ((self.x - (box_width / 2)), self.y,
                          box_width, box_height), 0)
        pygame.draw.rect(self.surface, box_edge_color,
                         ((self.x - (box_width / 2)), self.y,
                          box_width, box_height), 1)

        if len(message) != 0:
            self.surface.blit(self.font.render(message, 1, box_text_color),
                              (self.x - 100, self.y + 10))
        self.draw_counter()

        pygame.display.flip()

    def draw_counter(self):
        total_text = str(self.total_correct_words)
        set_text = str(self.n_correct_words)

        pygame.draw.rect(self.surface, (255, 255, 255),
                         ((self.x - 200), self.y + 175,
                          400, 60), 0)

        countertext_t = "Total correct words: " + total_text + \
                        "  Correct words this set: " + set_text
        text = self.font_counter.render(countertext_t, 1, counter_text_color)
        self.surface.blit(text, (self.x - 200, self.y + 180))

    def draw_input(self, correct):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.current_string = self.current_string[:-1]
                elif event.key == pygame.K_RETURN:
                    self.checker(string.join(self.current_string, ""),
                                 correct)
                    self.current_string = []
                elif event.key <= 127:
                    self.current_string.append(chr(event.key))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.prev_n_correct = self.n_correct_words
                self.prev_n_incorrect = self.n_incorrect_words
                self.n_correct_words = 0
                self.n_incorrect_words = 0
                self.current_string = []
                if self.x - (button_width / 2) <= event.pos[0] <= \
                   self.x + (button_width / 2) and \
                   self.y + 100 <= event.pos[1] <= self.y + 100 + \
                   button_height:
                    break

            self.draw_text_box(string.join(self.current_string, ""))

    def checker(self, word, cor_words):
        correct = cor_words
        word = word
        # check whether this word has been entered earlier
        if word in self.past_correct_words:
            self.surface.blit(self.font_feedback.render("Dit woord heb je "
                                                        "al gehad",
                              1, incorrect_color),
                              (self.x - 160, self.y - 70))
            pygame.display.flip()
            pygame.time.delay(800)
            pygame.draw.rect(self.surface, (255, 255, 255),
                             ((self.x - 200), self.y - 80,
                              400, 60), 0)
        # check whether this word is in the correct words list
        elif word in correct:
            self.surface.blit(self.font_feedback.render("Correct!",
                              1, correct_color),
                              (self.x - 55, self.y - 70))
            self.past_correct_words.append(word)
            self.n_correct_words += 1
            self.total_correct_words += 1
            pygame.display.flip()
            pygame.time.delay(800)
            pygame.draw.rect(self.surface, (255, 255, 255),
                             ((self.x - 200), self.y - 80,
                              400, 60), 0)
        # else this is not a correct word
        else:
            self.surface.blit(self.font_feedback.render("Incorrect",
                              1, incorrect_color),
                              (self.x - 60, self.y - 70))
            self.past_incorrect_words.append(word)
            self.n_incorrect_words += 1
            self.total_incorrect_words += 1
            pygame.display.flip()
            pygame.time.delay(800)
            pygame.draw.rect(self.surface, (255, 255, 255),
                             ((self.x - 200), self.y - 80,
                              400, 60), 0)


class Wait:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 25)

    def intro(self, image):
        self.surface.fill(background_color)
        self.surface.blit(image, (50, 50))

        pygame.display.flip()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

    def waiter(self, time=15000):
        self.surface.fill(background_color)
        text = self.font.render("Wacht op de volgende letterset", 1,
                                color_font)
        self.surface.blit(text, (self.x - 140, self.y))
        pygame.display.flip()
        pygame.time.delay(time)
        self.surface.fill(background_color)

    def outro(self):
        self.surface.fill(background_color)
        text = self.font.render("Dat was de eerste scrabbletaak!",
                                1, color_font)
        self.surface.blit(text, (self.x - 140, self.y - 30))
        text = self.font.render("Druk op de spatiebalk om verder te gaan",
                                1, color_font)
        self.surface.blit(text, (self.x - 170, self.y + 20))

        pygame.display.flip()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


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


class Main:
    def __init__(self, letters, words, subjectID, condition):
        # Init data collection
        self.start_time = timer()
        self.subjectID = subjectID
        self.condition = condition
        self.total_correct_n = 0
        self.total_incorrect_n = 0
        self.correct_input = []
        self.incorrect_input = []
        self.set_counter = -1

        filename = str(self.subjectID) + "_scrabble_pretest" + ".txt"
        f = open(filename, 'w')
        output = 'subjectID,condition,nth_set,letterset,time_start,time_end,' \
                 'time_in_set,correct_n,correct_words,incorrect_n,' \
                 'incorrect_words\n'
        f.write(output)
        f.close()

        # Init task
        pygame.init()
        self.surface = screen
        self.surface.fill(background_color)
        self.letters = letters
        self.word = words

        # Initiate objects
        self.indicator = list(range(len(stimulus_set)))
        self.stimulus = Stimulus(screen)
        self.user_input = Input(screen)
        self.wait = Wait(screen)
        self.button = Button(screen)

    def main(self):
        # Main loop
        clock = pygame.time.Clock()
        # Images should be in an 'images' folder
        image_intro01 = pygame.image.load(os.path.join("images", "intro_scrabble_pretest01.jpg")).convert()
        image_intro02 = pygame.image.load(os.path.join("images", "intro_scrabble_pretest02.jpg")).convert()
        self.wait.intro(image_intro01)
        self.wait.intro(image_intro02)

        for number in self.indicator:
            """Loop through letter sets and check input until next set
            button is clicked. Repeat until last set has been shown"""
            self.begin = timer()
            self.set_counter += 1
            self.stimulus.draw_letterset(self.letters[number])
            self.button.next_set()

            self.user_input.draw_input(correct_words[number])
            self.correct_input.append(self.user_input.past_correct_words)
            self.incorrect_input.append(self.user_input.past_incorrect_words)
            self.time = (timer() - self.begin)
            self.write_data(number)

            self.user_input.n_correct_words = 0
            self.user_input.n_incorrect_words = 0
            self.user_input.past_correct_words = []
            self.user_input.past_incorrect_words = []

            if self.set_counter + 1 == len(self.indicator):  # Check if this was the final set
                self.wait.outro()
                image_intro_foraging = pygame.image.load(os.path.join("images", "intro_practice_foraging.jpg")).convert()
                self.wait.intro(image_intro_foraging)
            else:
                self.wait.waiter(time=wait_time)

        screen.fill(background_color)
        clock.tick(fps)

    def write_data(self, number, filename=None):
        if filename is None:
            filename = str(self.subjectID) + "_scrabble_pretest" + ".txt"
        f = open(filename, 'a')
        output = str(self.subjectID) + "," + \
                 self.condition + "," + \
                 str(self.set_counter + 1) + "," + \
                 str(self.letters[number]) + "," + \
                 str(self.start_time) + "," + \
                 str(timer()) + "," + \
                 str(self.time) + "," + \
                 str(self.user_input.prev_n_correct) + "," + \
                 str(self.correct_input[self.set_counter]) + "," + \
                 str(self.user_input.prev_n_incorrect) + "," + \
                 str(self.incorrect_input[self.set_counter]) + "\n"
        f.write(output)
        f.close()

if __name__ == '__main__':
    subject_ID = sys.argv[1]
    if sys.argv[2] == "r":
        condition = random.choice(("c", "d"))
    else:
        condition = sys.argv[2]

    # Read letter set file
    stimulus_set = []
    with open('lettersets_pretest.csv', 'rb') as csvfile:
        letters = csv.reader(csvfile, delimiter=' ')
        for row in letters:
            stimulus_set.append(' '.join(row))

    # Read correct words file
    correct_words = []
    with open('words_pretest.csv', 'rU') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            correct_words.append(' '.join(row))
    for i in range(len(correct_words)):
        correct_words[i] = correct_words[i].split(',')

    run = Main(stimulus_set, correct_words, subject_ID, condition)
    run.main()
