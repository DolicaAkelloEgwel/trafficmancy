import pygame

from ask_question import ask_question
from traffic_counter import TrafficCounter

MODEL = "dolphin-phi"
traffic_counter = TrafficCounter()

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Trafficmancy")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)
response_text = ""
question_text = ""
input_active = True

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input_active = True
            question_text = ""
        elif event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:
                counts = traffic_counter.test()
                response_text = ask_question(MODEL, question_text, counts)
                question_text = ""
            elif event.key == pygame.K_BACKSPACE:
                question_text = question_text[:-1]
            else:
                question_text += event.unicode

        window.fill(0)
        text_surf = font.render(question_text, True, (255, 255, 255))
        window.blit(text_surf, text_surf.get_rect(center=window.get_rect().center))
        pygame.display.flip()

pygame.quit()
exit()
