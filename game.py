import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

def resize_frame(frame, width, height):
    if frame is not None:
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height

        new_width = width
        new_height = int(new_width / aspect_ratio)

        if new_height > height:
            new_height = height
            new_width = int(new_height * aspect_ratio)

        resized_frame = cv2.resize(frame, (new_width, new_height))
        return resized_frame
    else:
        return None

width, height = 1280, 720
pygame.init()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collect Money as much as you can")

fps = 30
clock = pygame.time.Clock()

external_webcam_index = 0
cap = cv2.VideoCapture(external_webcam_index)
cap.set(3, width)
cap.set(4, height)

imgmoney = pygame.image.load('./Resources/tk.jpg')
new_width = 150
new_height = 66.5
imgmoney = pygame.transform.scale(imgmoney, (new_width, new_height))

rectmoney = imgmoney.get_rect()
rectmoney.x, rectmoney.y = 500, 300

speed = 15
score = 0
startTime = time.time()
totalTime = 60

detector = HandDetector(detectionCon=0.8, maxHands=2)

def resetmoney():
    rectmoney.x = random.randint(100, width - 100)
    rectmoney.y = height + 50

start_game = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                start_game = True

    if start_game:
        timeRemain = int(totalTime - (time.time() - startTime))
        if timeRemain < 0:
            window.fill((255, 255, 255))
            font = pygame.font.Font(None, 50)
            textScore = font.render(f'Your Collect: BDT {score}', True, (50, 50, 255))
            textTime = font.render(f'Time UP', True, (50, 50, 255))
            window.blit(textScore, (450, 350))
            window.blit(textTime, (530, 275))
        else:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = resize_frame(img, width, height)
            hands, img = detector.findHands(img, flipType=False)
            rectmoney.y -= speed
            if rectmoney.y < 0:
                resetmoney()
                speed += 1
            for hand in hands:
                x, y = hand['lmList'][8][0:2]
                if rectmoney.collidepoint(x, y):
                    resetmoney()
                    score += 1000
                    speed += 1
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(imgmoney, rectmoney)
            font = pygame.font.Font(None, 50)
            textScore = font.render(f'BDT {score}', True, (50, 50, 255))
            textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
            window.blit(textScore, (35, 35))
            window.blit(textTime, (1000, 35))
    else:
        window.fill((255, 255, 255))
        font = pygame.font.Font(None, 50)
        textStart = font.render("Press SPACE to Start", True, (255, 0, 0))
        window.blit(textStart, (400, 300))
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
