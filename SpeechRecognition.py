
import pygame
import speech_recognition as sr
import random
import threading 
import sys

COLORS = {(255, 255, 255) : "White", (255, 0, 0) : "Red", (0, 255, 0) : "Green",  (0, 0, 255) : "Blue", (255,165,0) : "Orange", (255, 255, 0) : "Yellow", (128, 0, 128) : "Purple", (255,192,203) : "Pink", (139, 69, 19) : "Brown",  (128, 128, 128) : "Gray"}
WIDTH, HEIGHT = 800, 600
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

current_recognized_text = "None"

def Recognize_speech():   
    recognizer = sr.Recognizer()

    global is_listening
    is_listening = True
    while is_listening:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            global current_recognized_text
            try:
                text = recognizer.recognize_google(audio, language='eng-ENG')
                print("Вы сказали: " + text)
                current_recognized_text = text

            except sr.UnknownValueError:
                current_recognized_text = "None"
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания: {e}")
                current_recognized_text = "None"
            except sr.WaitTimeoutError as e:
                print(f"Ошибка сервиса распознавания: {e}")
                current_recognized_text = "None"

    print("Finish listening")

def think_color(previous_color = None):
    current_colors = list(COLORS.keys())
    if (previous_color in current_colors):
        current_colors.remove(previous_color)
    square_color = random.choice(current_colors)

    square_color_name = COLORS[square_color]
    print("think color name: ",square_color_name)

    return square_color, square_color_name

if __name__ == "__main__":
    bg = pygame.image.load('data/bg.jpg')

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Speech Recognition Game")

    is_running = True

    square_color, square_color_name = think_color()

    font = pygame.font.SysFont('Comic Sans MS', 30)
    say_color_surface = font.render('Say name of color in english', False, WHITE)

    clock = pygame.time.Clock()

    baloon = pygame.image.load('data/baloon.png')
    baloon.fill(square_color, special_flags=pygame.BLEND_RGB_MULT)

    microphone_thread = threading.Thread(target=Recognize_speech)
    microphone_thread.start()

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                global is_listening
                is_listening = False
                break

        said_text_surface = font.render('You said: ' + ('Can not recongnize' if (current_recognized_text == "None") else current_recognized_text), False, WHITE)

        if (current_recognized_text.lower() == square_color_name.lower()):
            print("Right")
            square_color, square_color_name = think_color(square_color)
            baloon = pygame.image.load('data/baloon.png')
            baloon.fill(square_color, special_flags=pygame.BLEND_RGB_MULT)

        screen.blit(bg, (-200, -100))
        screen.blit(say_color_surface, (200, 500))
        screen.blit(said_text_surface, (200, 550))

        screen.blit(baloon, (300, 70))

        pygame.display.flip()

        # Установка FPS
        clock.tick(FPS)

    if (microphone_thread.is_alive()):
        microphone_thread.join()

    pygame.quit()
    sys.exit()