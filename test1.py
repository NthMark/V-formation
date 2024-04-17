import sys
import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((50, 30), pg.SRCALPHA)
        color = pg.Color('dodgerblue1')
        pg.draw.polygon(self.image, color, ((1, 1), (20, 15), (1, 29)))
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(0, 0)
        self.speed = 2

    def update(self):
        self.rotate()
        self.pos += self.vel
        self.rect.center = self.pos

    def rotate(self):
        _, angle = (pg.mouse.get_pos()-self.pos).as_polar()
        self.vel.from_polar((self.speed, angle))
        self.image = pg.transform.rotozoom(self.orig_img, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((300, 200))
    all_sprites.add(player)

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player.speed += .2
        elif keys[pg.K_s]:
            player.speed -= .2

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()