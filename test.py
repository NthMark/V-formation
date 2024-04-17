import sys
import pygame as pg
from pygame.math import Vector2


def main():
    screen = pg.display.set_mode((640, 480))
    screen_rect = screen.get_rect()
    font = pg.font.Font(None, 30)
    color = pg.Color(150, 250, 100)
    clock = pg.time.Clock()
    pole = Vector2((20,30))
    pole1=Vector2(screen_rect.center)
    print(pole)
    # A zero vector.
    vec = Vector2()
    # To set the coordinates of `vec` we can pass the
    # polar coordinates (radius, angle) to `from_polar`.
    vec.from_polar((90, 45))
    print(vec)  # Now take a look at the updated cartesian coordinates.
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        mouse_pos = pg.mouse.get_pos()
        # `as_polar` gives us the radius and angle of the vector that
        # points to the mouse. Unpack it into the `r` and `phi` variables.
        r, phi = (mouse_pos-pole).as_polar()

        screen.fill((30, 30, 30))
        # Draw the line to the mouse pos.
        pg.draw.line(screen, color, pole, mouse_pos, 3)
        # Add the vec to the pole to get the target coordinates.
        pg.draw.line(screen, (200, 90, 20), pole, pole+vec, 3)
        pg.draw.line(screen, (200, 90, 20), pole1, pole1+vec, 3)
        # Render the radius and angle.
        txt = font.render('r: {:.1f}'.format(r), True, color)
        screen.blit(txt, (30, 30))
        txt = font.render('phi: {:.1f}'.format(phi), True, color)
        screen.blit(txt, (30, 50))

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()