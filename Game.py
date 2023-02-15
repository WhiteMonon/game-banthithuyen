from ast import walk
from asyncio import events
from asyncio.windows_events import NULL
from cProfile import label
from cgi import print_arguments
from email.mime import image
import imghdr
import imp
from importlib.metadata import files
import keyword
from math import fabs
from operator import truediv
import secrets
from select import select
from tkinter import W
import pygame
import sys
from pygame.sprite import Sprite
import time
import os
from pygame.sprite import Sprite , Group
import random

class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800 , 480))
        pygame.display.set_caption('Game Bắn Phi Thuyền')

        self.rect = self.screen.get_rect()

        self.bg = pygame.image.load('bg.jpg')
        self.bg = pygame.transform.scale(self.bg , (800 , 480))

        self.phithuyen = PhiThuyen(self)
        self.so_phi_thuyen = 3

        self.clock = pygame.time.Clock()

        self.dan = pygame.sprite.Group()
        # self.item_dan = pygame.sprite.Group()
        # self.tao_item_dan()

        self.quaivat = pygame.sprite.Group()
        self.speed_Qv = 2
        
        quaivat = QuaiVat(self)
        self.qv = QuaiVat(self)
        #self.quaivat.add(quaivat)
        
        self.so_quai_vat = self.screen.get_width() // (quaivat.rect.width * 2)
        self.so_hang = (self.screen.get_height() //2) // (quaivat.rect.height * 2)

        self.tao_quai_vat()

        self.btn_play =  Button(self , 'Play')

        self.dang_choi = False

        self.vu_no = pygame.sprite.Group()

        
        
        # bang diem
        self.diem = 0
        self.ky_luc = 0
        self.bang_diem = BangDiem(self)
        self.bang_diem = BangDiem(self)

        # Am thanh
        pygame.mixer.music.load('backgroundMusic.mp3')
        pygame.mixer.music.play(-1)

        self.ban = pygame.mixer.Sound('piupiu.mp3')
        self.no = pygame.mixer.Sound('tiengno.wav')

    # def tao_item_dan(self):
    #     dan = Dan(self)
    #     self.item_dan.add(dan)

    def tao_quai_vat(self):
        quaivat = QuaiVat(self)
        #self.quaivat.add(quaivat)
        
        so_quai_vat = self.screen.get_width() // (quaivat.rect.width * 2)
        so_hang = (self.screen.get_height() //2) // (quaivat.rect.height * 2)

        for i in range(so_quai_vat):
            for j in range(so_hang):
                qv = QuaiVat(self)
                qv.rect.x = qv.rect.width * i * 2
                qv.rect.y = qv.rect.height * j*2
                self.quaivat.add(qv)

    # event handling
    def evehand(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.phithuyen.phai = True
                        self.phithuyen.quay_mat = False
                    if event.key == pygame.K_LEFT:
                        self.phithuyen.trai = True
                        self.phithuyen.quay_mat = True
                    if event.key == pygame.K_UP:
                        self.phithuyen.len = True
                        
                    if event.key == pygame.K_DOWN:
                        self.phithuyen.xuong = True
                    if event.key == pygame.K_SPACE:
                        if self.dang_choi is True:
                            #self.tao_item_dan()
                            if self.phithuyen.so_tia_dan % 2 == 0:
                                for i in range (self.phithuyen.so_tia_dan):
                                    dan = Dan(self)
                                    w = dan.rect.width
                                    dan.rect.x += (-1)**i*w*(i//2 + 1/2)
                                    self.dan.add(dan)
                            else:
                                for i in range (self.phithuyen.so_tia_dan):
                                    dan = Dan(self)
                                    w = dan.rect.width
                                    dan.rect.x += (-1)**i*w*((i+1)//2)
                                    self.dan.add(dan)
                            pygame.mixer.Sound.play(self.ban)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.phithuyen.phai = False
                    if event.key == pygame.K_LEFT:
                        self.phithuyen.trai = False
                    if event.key == pygame.K_UP:
                        self.phithuyen.len = False
                    if event.key == pygame.K_DOWN:
                        self.phithuyen.xuong = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.phithuyen.chuotxuong = True

                    mouse = pygame.mouse.get_pos()

                    clicked = self.btn_play.rect.collidepoint(mouse)

                    if clicked and not self.dang_choi:
                        self.dang_choi = True
                        self.so_phi_thuyen = 3
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.phithuyen.chuotxuong = False
    
    def moveOfmonter(self):
        for quaivat in self.quaivat.sprites():
                quaivat.draw()
                if (quaivat.rect.right >= self.rect.width):
                    quaivat.phai = False
                    quaivat.trai = True
                    quaivat.rect.y += quaivat.rect.height
                elif (quaivat.rect.left < 0):
                    quaivat.trai = False
                    quaivat.phai = True
                    quaivat.rect.y += quaivat.rect.height

    def removeBullet(self):
        for dan in self.dan.sprites():
                if dan.rect.bottom <= 0:
                    self.dan.remove(dan)

    def collishand(self):
        va_cham = pygame.sprite.groupcollide(self.dan , self.quaivat , True , True)

        if va_cham:
            vuno = VuNo(self)
            for vacham in va_cham:
                vuno.rect.center = vacham.rect.center
                self.vu_no.add(vuno)
            pygame.mixer.Sound.play(self.no)
            for quai_vat in va_cham.values():
                self.diem += 50 * len(quai_vat)
                self.bang_diem.kiem_tra_ky_luc(self)
            self.bang_diem.tinh_diem(self)
        
        
        if pygame.sprite.spritecollideany(self.phithuyen , self.quaivat):
            self.quaivat.empty()
            self.dan.empty()
            self.phithuyen.rect.midbottom = self.rect.midbottom
            self.so_phi_thuyen -= 1
            self.bang_diem.tinh_so_mang(self)
            time.sleep(1)
            self.tao_quai_vat()
    
    def kiem_tra(self):
        for quaivat in self.quaivat.sprites():
            if quaivat.rect.bottom >= self.rect.bottom:
                self.dan.empty()
                self.quaivat.empty()
                self.phithuyen.rect.midbottom = self.rect.midbottom
                self.so_phi_thuyen -= 1
                self.bang_diem.tinh_so_mang(self)
                time.sleep(1)
                break


    def main(self):
        while True:
            self.clock.tick(60)
            
            self.evehand()

            self.screen.blit(self.bg , (0,0))
            self.phithuyen.draw()

            for dan in self.dan.sprites():
                dan.draw()
            # for dan in self.item_dan.sprites():
            #     dan.draw()
            if self.dang_choi:
                
                self.phithuyen.update()

                self.dan.update()

                #self.item_dan.update()

                self.quaivat.update()

                self.vu_no.update()
                

            self.collishand()

            for vuno in self.vu_no.sprites():
                vuno.draw()
                if vuno.xoa is True:
                    self.vu_no.remove(vuno)

            if not self.quaivat:
                #self.dan.empty()
                self.tao_quai_vat()
                self.phithuyen.so_tia_dan += 1
                self.speed_Qv += 2
                

            self.removeBullet()

            self.moveOfmonter()

            if self.dang_choi is False:
                self.btn_play.draw()

            for quaivat in self.quaivat.sprites():
                if(quaivat.rect.y >= self.rect.height):
                    self.quaivat.remove(quaivat)
            
            self.bang_diem.draw()

            self.kiem_tra()
            

            pygame.display.flip()

            if self.so_phi_thuyen == 0:
                self.dang_choi = False
                self.diem = 0
                self.bang_diem.tinh_diem(self)
                self.so_phi_thuyen = 3
                self.phithuyen.so_tia_dan = 1
                self.bang_diem.tinh_so_mang(self)

# class Item_Dan(Sprite):
#     def __init__(self , game):
#         super().__init__()

#         self.speed = 5

#         self.screen = game.screen
#         self.image = pygame.image.load('bullet.png')
#         self.image = pygame.transform.scale(self.image , (25 , 25))
#         self.rect = self.image.get_rect()
#         self.rect.x = random.randint(0 , 800)

#     def draw(self):
#         self.screen.blit(self.image , self.rect)
#     def update(self):
#         self.rect.y += self.speed
class PhiThuyen(Sprite):
    def __init__(self , game):
        super().__init__()
        
        self.trai = False
        self.phai = False
        self.len = False
        self.xuong = False
        self.chuotxuong = False
        self.kich_thuoc_phi_thuyen = (50 , 40)
        
        self.speed = 5
        self.so_tia_dan = 1

        self.rectofgame = game.rect
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()


        self.obj = pygame.image.load('phithuyen.png')
        self.obj = pygame.transform.scale(self.obj , self.kich_thuoc_phi_thuyen)
        self.rect = self.obj.get_rect()

        self.image = self.obj

        self.rect.midbottom = self.screen_rect.midbottom

        self.qua_phai = []
        self.qua_trai = []
        self.quay_mat = False
        self.index = 0
        

    def draw(self):
        self.screen.blit(self.obj , self.rect)
    def update(self):
        self.moveLeft()
        self.moveRight()
        self.moveDown()
        self.moveUp()
        self.movetoMousePos()
        self.chuyen_dong()

    def moveLeft(self):
        if (self.trai and self.rect.x > 0):
            self.rect.x -= self.speed
    def moveRight(self):
         if (self.phai and self.rect.x < self.rectofgame.width - self.rect.width):
            self.rect.x += self.speed
    def moveUp(self):
        if (self.len and self.rect.y > 0):
            self.rect.y -= self.speed
    def moveDown(self):
        if (self.xuong and self.rect.y < self.rectofgame.height - self.rect.height):
            self.rect.y += self.speed
    def movetoMousePos(self):
        self.mousepos = pygame.mouse.get_pos()
        if (self.chuotxuong):
            if (self.rect.centerx < self.mousepos[0] ):
                self.rect.centerx += self.speed
            if (self.rect.centerx > self.mousepos[0]):
                self.rect.centerx -= self.speed
            if (self.rect.centery < self.mousepos[1]):
                self.rect.centery += self.speed
            if (self.rect.centery > self.mousepos[1]):
                self.rect.centery -= self.speed
    def lay_anh(self , path):
        ds_anh_phai =[]
        ds_anh_trai =[]
        for _,_, files in os.walk(path):
            for file in files:
                img = pygame.image.load(path + file)
                img = pygame.transform.scale(img , self.kich_thuoc_phi_thuyen)
                ds_anh_phai.append(img)
                img = pygame.transform.flip(img , True , False)
                ds_anh_trai.append(img)
        return ds_anh_phai , ds_anh_trai

    def chuyen_dong(self):
        self.qua_phai , self.qua_trai = self.lay_anh('./phithuyenphai/')
        if (self.quay_mat == False):
            if self.phai is True:
                self.obj = self.qua_phai[self.index]
                self.index += 1
                if self.index == len(self.qua_phai):
                    self.index = len(self.qua_phai) - 1
            else:
                self.can_bang()
        else:
            if (self.trai):
                self.obj = self.qua_trai[self.index]
                self.index += 1
                if self.index == len(self.qua_phai):
                    self.index = len(self.qua_phai) - 1
            else:
                self.can_bang()

    def can_bang(self):
        while self.index >= 0:
            self.obj = self.qua_phai[self.index]
            self.index -=1
        self.index = 0

        if (self.index == 0 and self.len):
            self.bay_len()
    def bay_len(self):
        if (self.len):
            self.obj = pygame.image.load('phithuyenlen.png')
            self.obj = pygame.transform.scale(self.obj , self.kich_thuoc_phi_thuyen)
        else:
            self.obj = pygame.image.load('phithuyen.png')
            self.obj = pygame.transform.scale(self.obj , self.kich_thuoc_phi_thuyen)

class Dan(Sprite):
    def __init__(self , game):
        super().__init__()

        self.speed = 5
        self.spacedown = False

        self.screen = game.screen
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image , (25 , 25))
        self.rect = self.image.get_rect()

        self.rect.midbottom = game.phithuyen.rect.midtop
    def draw(self):
        self.screen.blit(self.image , self.rect)
    def update(self):
        self.rect.y -= self.speed

class QuaiVat(Sprite):
    def __init__(self , game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.rect

        #self.speed = 2

        self.trai = False
        self.phai = True

        self.image = pygame.image.load('monter.png')
        self.image = pygame.transform.scale(self.image , (50 , 50))
        self.rect = self.image.get_rect()

        #self.rect.midtop = self.screen_rect.midtop
    def draw(self):
        self.screen.blit(self.image , (self.rect.x , self.rect.y + 30))
    def update(self):
        if (self.phai):
            self.rect.x += game.speed_Qv
        elif (self.trai):
            self.rect.x -= game.speed_Qv

class Button:
    def __init__(self , game , label):
        self.screen = game.screen
        self.screen_rect = game.rect

        self.width = 100
        self.height = 50
        self.text_color = 'white'
        self.color = 'green'
        self.font = pygame.font.SysFont(None , 50)

        self.rect = pygame.Rect(0 , 0 , self.width , self.height )
        self.rect.center = self.screen_rect.center

        self.text = self.font.render(label , True , self.text_color , self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.screen_rect.center
    def draw(self):
        self.screen.fill(self.color , self.rect)
        self.screen.blit(self.text , self.text_rect)

class VuNo(Sprite):
    def __init__(self , game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.rect

        self.xoa = False

        self.ds_anh = []
        for _, _, files in os.walk('./no'):
            for file in files:
                img = pygame.image.load('./no/' + file)
                img = pygame.transform.scale(img , (75 , 75))
                self.ds_anh.append(img)
        self.index = 0
        self.image = self.ds_anh[self.index]
        self.rect = self.image.get_rect()
    def draw(self):
        self.screen.blit(self.image , self.rect)
    def update(self):
        self.index += 1
        if self.index == len(self.ds_anh) - 1:
            self.xoa = True
        self.image = self.ds_anh[self.index]

class BangDiem:
    def __init__(self,game):
        self.screen = game.screen
        self.screen_rect = game.rect

        self.color = (255 , 255 ,255)
        self.font = pygame.font.SysFont(None , 50)
        self.tinh_diem(game)
        self.tinh_ky_luc(game)
        self.kiem_tra_ky_luc(game)
        self.tinh_so_mang(game)
        
    def draw(self):
        self.screen.blit(self.text , self.rect)
        self.screen.blit(self.ky_luc , self.ky_luc_rect)
        self.phi_thuyen.draw(self.screen)
    def tinh_diem(self , game):
        self.text = self.font.render(str(game.diem) , True , self.color)
        self.rect = self.text.get_rect()
        self.rect.left = 5
        self.rect.top = 0
    def tinh_ky_luc(self , game):
        self.ky_luc = self.font.render(str(game.ky_luc) , True , self.color)
        self.ky_luc_rect = self.ky_luc.get_rect()
        self.ky_luc_rect.midtop = game.rect.midtop
    def kiem_tra_ky_luc(self , game):
        if game.diem > game.ky_luc:
            game.ky_luc = game.diem
            self.tinh_ky_luc(game)
    def tinh_so_mang(self,game):
        self.phi_thuyen = Group()
        for i in range (game.so_phi_thuyen):
            phi_thuyen = PhiThuyen(game)
            phi_thuyen.rect.topright = game.rect.topright
            phi_thuyen.rect.x -= i*phi_thuyen.rect.width
            self.phi_thuyen.add(phi_thuyen)
if __name__ == '__main__':
    game = Game()
    game.main()