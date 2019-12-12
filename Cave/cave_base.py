# cave - Copyright 2016 Kenichiro Tanaka

import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

# pygame 초기화
pygame.init()
# 키의 반복 기능 설정
pygame.key.set_repeat(5, 5)
# 화면 크기 설정
SURFACE = pygame.display.set_mode((800, 600))
# 프레임 레이트 조정용의 타이머
FPSCLOCK = pygame.time.Clock()

def main():
    # 메인 루틴
    # 동굴을 구성하는 직사각형의 수
    walls = 80
    # 내 캐릭터의 Y 좌표
    ship_y = 250
    # 내 캐릭터가 상하로 이동할 때의 속도
    velocity = 0
    # 점수
    score = 0
    # 동굴의 기울기(옆의 직사각형과 Y축 방향으로 얼마나 비켜 있는지)
    slope = randint(1, 6) 
    sysfont = pygame.font.SysFont(None, 36)
    # 내 캐릭터 이미지
    ship_image = pygame.image.load("ship.png")
    # 내 캐릭터 크기 조절 
    ship_image = pygame.transform.scale(ship_image, (50, 50))
    # ship_image = Image.open('ship.png')
    # 폭발 이미지
    bang_image = pygame.image.load("bang.png")
    # 폭발 이미지 크기 조절
    bang_image = pygame.transform.scale(bang_image, (140, 140))
    # 동굴을 구성하는 직사각형을 저장하는 배열
    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))
    # 게임 오버인지 아닌지 여부의 플래그
    game_over = False

    while True:
        is_space_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True

        # 내 캐릭터를 이동
        # 게임 중 일때
        if not game_over:
            # 점수 10 증가
            score += 10
            # 스페이스 키 입력 상태에 따른 속도 -3(상승) 또는 +3(하강)
            velocity += -3 if is_space_down else 3
            ship_y += velocity

            # 동굴을 스크롤
            edge = holes[-1].copy()
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20)
            edge.move_ip(10, slope)
            # 맨 끝(오른쪽 끝)에 추가
            holes.append(edge)
            # 맨 앞의 직사각형을 삭제
            del holes[0]
            # 전체를 왼쪽으로 10 이동
            holes = [x.move(-10, 0) for x in holes]

            # 충돌 ?
            # 내 캐릭터가 동굴 벽에 충돌했는지 판정
            if holes[0].top > ship_y or holes[0].bottom < ship_y + 80:
                game_over = True

        # 그리기
        # 녹색으로 전체 화면 채우기
        SURFACE.fill((0, 255, 0))
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
        SURFACE.blit(ship_image, (0, ship_y))
        score_image = sysfont.render("Score is {}".format(score), True, (0, 0, 255))
        SURFACE.blit(score_image, (600, 20))

        if game_over:
            SURFACE.blit(bang_image, (0, ship_y - 40))

        # 그리기를 화면에 반영
        pygame.display.update()
        # 타이머를 사용해서 FPS를 조정
        FPSCLOCK.tick(15)


if __name__ == '__main__':
    main()    
