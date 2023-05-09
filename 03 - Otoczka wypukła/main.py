import pygame
import random

import logging 

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("log.txt")
formatter = logging.Formatter("%(asctime)s    %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

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
num_points = 4


def get_orientation(p, q, r):
    # zwraca wartość > 0, jeśli p->q->r skręca w lewo (w lewo od wektora pq)
    # wartość < 0, jeśli p->q->r skręca w prawo (w prawo od wektora pq)
    # wartość == 0, jeśli punkty są współliniowe
    # funkcja pomocnicza do obliczenia orientacji względem kolejnych punktów
    return (q[1]-p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])


def refresh_drawing_surface(): 
    screen.blit(drawing_surface, drawing_rect)
    screen.blit(log_surface, (0, screen_height - LOG_HEIGHT))
    pygame.display.flip()
    
    
def find_lowest_y_or_highest_x_iterative(n, points, primary_color, secondary_color):
    draw_text("Wyszukiwanie punktu o najmniejszej współrzędnej y lub o największej x...")
    print("Finding lowest y or highest x")
    
    start = 0
    point = pygame.draw.circle(drawing_surface, secondary_color, points[start], 4)
    drawn_elements.append(point)
    
    for i in range(1, n):
        if points[i][1] < points[start][1] or (points[i][1] == points[start][1] and points[i][0] > points[start][0]):
            pygame.draw.circle(drawing_surface, primary_color, points[start], 4)
            start = i
            pygame.draw.circle(drawing_surface, secondary_color, points[start], 4)
        draw_text(f"Wybrany punkt {points[start]} - sprawdzany punkt {points[i]}")
        pygame.time.wait(300)
    pygame.draw.circle(drawing_surface, primary_color, points[start], 4)
    return start


def gift_wrap(points):
    n = len(points)
    hull = []

    start = find_lowest_y_or_highest_x_iterative(n, points, green, orange)

    while True:
        hull.append(start)
        draw_text(f"Sprawdzam linie dla punktu {points[start]}...")
        end = (start + 1) % n
        for i in range(n):
            pygame.draw.circle(drawing_surface, orange, points[start], 4)
            pygame.draw.circle(drawing_surface, pink, points[i], 4)
            pygame.draw.circle(drawing_surface, orange, points[end], 4)
            draw_text(f"Sprawdzam orientację punktu {points[i]} względem punktu {points[start]}.")
            
            pygame.draw.line(drawing_surface, pink, points[start], points[i], 1)
            
            orientation = get_orientation(points[start], points[i], points[end])
            print("Orientation:", orientation)
            refresh_drawing_surface()
            pygame.time.wait(300)
            
            pygame.draw.line(drawing_surface, white, points[start], points[i], 1)
            
            if orientation < 0:
                draw_text(f"Punkt {points[i]} jest po lewej stronie wektora {points[start]} - {points[end]}.")
                pygame.draw.line(drawing_surface, blue, points[start], points[i], 1)
                end = i
            else:
                draw_text(f"Punkt {points[i]} jest po prawej stronie wektora {points[start]} - {points[end]}.")
                pygame.draw.line(drawing_surface, white, points[start], points[i], 1)
                
            refresh_drawing_surface()
            pygame.time.wait(300)
            
            pygame.draw.circle(drawing_surface, black, points[i], 4)
            pygame.draw.circle(drawing_surface, black, points[end], 4)
            
            refresh_drawing_surface()
            pygame.time.wait(300)
            
        pygame.draw.circle(drawing_surface, black, points[start], 4)
        pygame.draw.line(drawing_surface, green, points[start], points[end], 1)
            
        draw_text(f"Dla punktu {points[start]} wybrano punkt {points[end]}.")
        start = end
        if start == hull[0]:
            pygame.draw.circle(drawing_surface, (0,0,255), points[start], 4)
            refresh_drawing_surface()
            pygame.time.wait(300)
            break

    return [points[i] for i in hull]


# rysowanie punktów
def draw_points(points):
    for p in points:
        pygame.draw.circle(drawing_surface, black, p, 4)
        refresh_drawing_surface()
        pygame.time.wait(300)


# rysowanie otoczki wypukłej
def draw_hull(hull, color, line_width=1):
    draw_text("Rysuję otoczkę wypukłą...")
    if len(hull) <= 1:
        return
    for i in range(len(hull)):
        start = i
        end = (i+1) % len(hull)
        print(f"Drawing line from {start} - {hull[start]} to {end} - {hull[end]}")
        draw_text(f"Rysuję linię z punktu {hull[start]} do punktu {hull[end]}...")
        line = pygame.draw.line(drawing_surface, color, hull[start], hull[end], line_width)
        drawn_elements.append(line)
        # wyświetlenie zawartości ekranu
        refresh_drawing_surface()
        
        pygame.time.wait(300)
        
    if check_if_hull_points_have_identical_coordinates(hull):
        draw_text("Otoczka wypukła jest punktem.")
    elif check_if_one_coordinate_is_identical(hull):
        draw_text("Otoczka wypukła jest linią.")
    elif check_hull_is_triangle(hull):
        draw_text("Otoczka wypukła jest trójkątem.")
    else:
        draw_text(f"Otoczka wypukła jest czworokątem.")
    
    draw_text(f"Otoczka wypukła została narysowana. Punkty {hull}")
    
    
def check_if_hull_points_have_identical_coordinates(hull):
    return len(set(hull)) == 1


def check_if_one_coordinate_is_identical(hull):
    x = list(set([p[0] for p in hull]))
    y = list(set([p[1] for p in hull]))
    return (len(x) == 1 or len(y) == 1) and len(hull) > 1


def check_hull_is_triangle(hull):
    x = list(set([p[0] for p in hull]))
    y = list(set([p[1] for p in hull]))
    return (len(x) == 2 or len(y) == 2) and len(hull) == 3
        

def draw_text(text):
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
    finished = True
    
    while running:
        clear_screen()
        
        draw_text("Generowanie punktów...")
        
        if len(points) > 4:
            draw_text("Zbyt dużo punktów. Wybierz mniej niż 5.")
            break

        draw_text("Rysowanie punktów...")
        draw_points(points)
        
        # wyświetlenie zawartości ekranu
        pygame.display.flip()

        # wizualizacja algorytmu Jarvisa
        jarvis_hull = gift_wrap(points)
        draw_hull(jarvis_hull, red)
        
        while finished:
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
