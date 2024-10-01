import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect):
    """
    引数：こうかとん、または、爆弾のRect
    戻り値:真偽値タプル(横判定結果、縦判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False

    return yoko, tate

def game_over(screen: pg.Rect):
    """
    ゲームオーバーになった時に画面にこうかとんとゲームオーバーの文字列を表示する関数
    """
    img = pg.image.load("fig/8.png")
    font = pg.font.Font(None, 55)
    # 描画する文字列の設定（白色）
    game_over_rect = pg.Rect(0, 0, WIDTH, HEIGHT)
    pg.draw.rect(screen, (255, 0, 0), game_over_rect, 0)
    text = font.render("GAME OVER", True, (255, 255, 255))
    # 文字列の表示位置
    screen.blit(text, [WIDTH/2, HEIGHT/2])
    screen.blit(img, [WIDTH/4, HEIGHT/2])
    screen.blit(img, [WIDTH*3/4, HEIGHT/2])
    pg.display.update()
    time.sleep(3)

def bomb_list():
    """
    爆弾の加速度と大きさを10段階で表すリストの作成
    """
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_imgs.append(bb_img)

        return accs, bb_imgs




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # bb_img = pg.Surface((20, 20))  # 空のSurface
    # bb_img.set_colorkey((0, 0, 0))  # 爆弾の四隅を透過させる
    # pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    # bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    # bb_rct.centerx = random.randint(0, WIDTH)
    # bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    bb_accs, bb_imgs = bomb_list()
    avx = vx*bb_accs[min(tmr//500, 9)]
    bb_img = bb_imgs[min(tmr//500, 9)]
    bb_img.set_colorkey((0, 0, 0)) 
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 横座標, 縦座標
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            screen.blit(kk_img, kk_rct)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, vy)
        screen.blit(bb_img, bb_rct)
        bb_rct.move_ip(avx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            avx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()


