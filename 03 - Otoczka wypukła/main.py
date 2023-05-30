import pygame
import random

import logging 
import math

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("log.txt")
formatter = logging.Formatter("%(asctime)s    %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

WAIT_TIME = 250

pygame.init()

# ustawienia okna
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Otoczka wypukła")

drawn_elements: list[pygame.Rect] = []

# kolory
white = (255, 255, 255)
light_grey = (220, 220, 220)
black = (0, 0, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)
orange = (255, 165, 0)
blue = (0, 0, 255)
pink = (255, 0, 255)
green = (50, 255, 50)

# pole loga
LOG_WIDTH = screen_width
LOG_HEIGHT = 100
FONT_SIZE = 16
log_surface = pygame.Surface((LOG_WIDTH, LOG_HEIGHT))
log_surface.fill((220, 220, 220)) # kolor tła
log_rect = log_surface.get_rect()

# pole tekstowe
font = pygame.font.Font(None, FONT_SIZE)
padding = 10

# pole do rysowania
drawing_rect = pygame.Rect(0, 0, screen_width, screen_height - log_rect.height)
drawing_surface = pygame.Surface(drawing_rect.size)
drawing_surface.fill(white)

# ustawienia punktów
num_points = 5


def calculate_distance_between_two_points(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def get_orientation(segment, r):
    p, q = segment
    # zwraca wartość > 0, jeśli p->q->r skręca w lewo (w lewo od wektora pq)
    # wartość < 0, jeśli p->q->r skręca w prawo (w prawo od wektora pq)
    # wartość == 0, jeśli punkty są współliniowe
    # funkcja pomocnicza do obliczenia orientacji względem kolejnych punktów
    result = (q[1]-p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])
    if result == 0:
        print("Punkty są współliniowe", result)
    elif result > 0:
        print("Punkty skręcają w lewo", result)
    else:
        print("Punkty skręcają w prawo", result)
    return result
        

def refresh_drawing_surface(): 
    screen.blit(drawing_surface, drawing_rect)
    screen.blit(log_surface, (0, screen_height - LOG_HEIGHT))
    pygame.display.flip()
    

def find_point_with_max_x(points):
    max_x = None
    max_x_idx = 0
    for idx, point in enumerate(points):
        if idx == 0:
            max_x = point[max_x_idx]
            continue
        if point[0] > max_x:
            max_x = point[0]
            max_x_idx = idx
    return max_x_idx


def jarvis(points):        
    index_of_point_with_max_x = find_point_with_max_x(points)
    selected_point_idx = index_of_point_with_max_x
    hull = []
    hull_idx = 0
    selected_point = points[selected_point_idx]
    while True:
        draw_text(f"Wyszukuję punkt dla {selected_point}...")
        hull.append(selected_point)
        next_point = points[0]
        
        for point in points:
            draw_text(f"Sprawdzam punkt {point}...")
            
            original_next_point = next_point
            draw_segment((selected_point, next_point), pink, orange)
            pygame.draw.circle(drawing_surface, pink, point, 4)
            refresh_drawing_surface()
            pygame.time.wait(WAIT_TIME)
            
            draw_text(f"Sprawdzam orientację dla punktu {point} względem odcinka [{selected_point}, {next_point}]...")
            
            if next_point != hull[hull_idx] and get_orientation((selected_point, next_point), point) > 0:
                next_point = point
                draw_text(f"Kandydat {next_point} na podstawie orientacji względem odcinka [{selected_point}, {next_point}].")
            elif get_orientation((selected_point, next_point), point) == 0:
                draw_text(f"Sprawdzam odległość dla punktu {point}...")
                if calculate_distance_between_two_points(selected_point, next_point) < calculate_distance_between_two_points(selected_point, point):
                    next_point = point
                    draw_text(f"Kandydat {next_point} na podstawie odległości od {selected_point}.")
                else:
                    draw_text(f"Punkt {point} nie spełnia warunków.")
            else:
                draw_text(f"Punkt {point} nie spełnia warunków.")
                
            draw_segment((selected_point, original_next_point), white, black)
            draw_segment((selected_point, next_point), white, orange)
            pygame.draw.circle(drawing_surface, black, point, 4)
            refresh_drawing_surface()
            pygame.time.wait(WAIT_TIME)
            
        hull_idx += 1
        
        draw_segment((selected_point, next_point), green, orange)
        draw_segment((selected_point, next_point), white, black)
        
        selected_point = next_point
        
        draw_text(f"Wybrano punkt {selected_point} jako kolejny punkt na obwodzie otoczki.")
        
        if next_point == hull[0]:
            draw_text("Znaleziono punkt początkowy - koniec.")
            break
        
    return hull


def draw_segment(segment, segment_color, point_color):
    selected_point, next_point = segment
    pygame.draw.line(drawing_surface, segment_color, selected_point, next_point, 1)
    pygame.draw.circle(drawing_surface, point_color, selected_point, 4)
    pygame.draw.circle(drawing_surface, point_color, next_point, 4)
    refresh_drawing_surface()
    pygame.time.wait(WAIT_TIME)
    

# rysowanie punktów
def draw_points(points):
    for p in points:
        pygame.draw.circle(drawing_surface, black, p, 4)
        refresh_drawing_surface()
        pygame.time.wait(WAIT_TIME)


# rysowanie otoczki wypukłej
def draw_hull(hull, color=red, line_width=1):
    draw_text("Rysuję otoczkę wypukłą...")
    draw_text(f"Punkty otoczki: {hull}")
    if len(hull) <= 0:
        return
    for i in range(len(hull)):
        if len(hull) == 2 and i == 1:
            draw_text("Pomijam rysowanie ostatniego odcineka, bo jest identyczny z pierwszym.")
            continue
        current_point = hull[i]
        next_point = hull[(i+1) % len(hull)]
        print(f"Drawing line from {current_point} to {next_point}")
        draw_text(f"Rysuję linię z punktu {current_point} do punktu {next_point}...")
        line = pygame.draw.line(drawing_surface, color, current_point, next_point, line_width)
        drawn_elements.append(line)
        # wyświetlenie zawartości ekranu
        refresh_drawing_surface()
        pygame.time.wait(WAIT_TIME)
    
    if len(hull) == 1:
        draw_text("Otoczka wypukła jest punktem.")
    elif len(hull) == 2:
        draw_text("Otoczka wypukła jest odcinkiem.")
    else:
        draw_text(f"Otoczka wypukła jest {len(hull)}-kątem.")
    
    draw_text(f"Otoczka wypukła została narysowana. Punkty {hull}.")
    
        

def draw_text(text):
    print(text)
    logger.info(text)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.left = log_surface.get_rect().left
    log_surface.scroll(0, FONT_SIZE)
    log_surface.fill(light_grey, (0, 0, LOG_WIDTH, FONT_SIZE))
    log_surface.blit(text_surface, text_rect)
    refresh_drawing_surface()


def generate_random_points(num_points):
    return[
        (
            random.randint(padding, drawing_rect.width-padding), 
            random.randint(padding + log_rect.height, drawing_rect.height-padding)
        ) 
        for _ in range(num_points)
    ]


def clear_screen():
    drawing_surface.fill(white)
    screen.fill(white)
    pygame.display.flip()
    
    
def main(points):
    running = True
    global WAIT_TIME
    
    while running:
        finished = False
        clear_screen()
        
        draw_text("Generowanie punktów...")
        
        if len(points) > num_points:
            draw_text("Zbyt dużo punktów. Wybierz mniej niż 5.")
            break

        draw_text("Rysowanie punktów...")
        draw_points(points)
        
        # wyświetlenie zawartości ekranu
        pygame.display.flip()

        # wizualizacja algorytmu Jarvisa
        jarvis_hull = jarvis(points)
        draw_hull(jarvis_hull, red)
        
        draw_text("Naciśnij ENTER, aby uruchomić ponownie.")
        draw_text("Naciśnij ESC lub Q, aby zakończyć.")
        draw_text("Naciśnij K lub L, aby zmniejszyć lub zwiększyść szybkość animacji.")
        
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        running = False
                        finished = True
                    if event.key == pygame.K_RETURN:
                        finished = True
                    if event.key == pygame.K_k:
                        WAIT_TIME = WAIT_TIME - 50 if WAIT_TIME > 50 else 50
                        draw_text(f"Zmieniono czas oczekiwania na {WAIT_TIME} ms.")
                    if event.key == pygame.K_l:
                        WAIT_TIME = WAIT_TIME + 50 if WAIT_TIME < 1000 else 10000
                        draw_text(f"Zmieniono czas oczekiwania na {WAIT_TIME} ms.")
                elif event.type == pygame.QUIT:
                    running = False
                    finished = True
            
            pygame.time.wait(100)

    pygame.quit()

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Program wizualizujący otoczkę wypukłą.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--random', action='store_true', help='Losowy zestaw czterech punktów')
    group.add_argument('-n', '--numbers', type=str, help="Wpisz punkty, przykład: \"(1,1),(2,2),(3,3)\"")

    args = parser.parse_args()
    
    if args.random:
        points = generate_random_points(num_points)
    elif args.numbers:
        points = [tuple(map(int, x.split(','))) for x in args.numbers.strip('()').split('),(')]
    else:
        sys.exit("Nie podano argumentów. Użyj -h lub --help, aby uzyskać pomoc.")
        
    try:
        main(points)
    except KeyboardInterrupt:
        logger.info("Przerwano działanie programu.")
