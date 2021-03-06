"""
v1.5 新增功能：
    1.优化坦克的移动方式
        按下方向键坦克持续移动
        松开方向键坦克停止移动
"""
import pygame,time
# 将pygame.display 简称为_display
_display = pygame.display
COLOR_RED = pygame.Color(255,0,0)
version= 'v1.4'
#游戏主逻辑类
class MainGame():
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 550
    #窗口对象
    window = None
    PI_TANK = None
    #开始游戏
    def startGame(self):
        pygame.display.init()
        #加载游戏窗口()
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT])
        #设置游戏标题
        pygame.display.set_caption('坦克大战'+version)
        #创建一个坦克
        MainGame.PI_TANK = Tank(600,220)
        while True:
            #渲染背景
            MainGame.window.fill(pygame.Color(0,0,0))
            #调用事件处理的方法
            self.getEvent()
            #将带有文字的surface绘制到窗口中
            MainGame.window.blit(self.drawText('剩余敌方坦克%d辆'%5),(5,5))
            #加载我方坦克 display_tank()中实现了两件事：1.根据方向修改图片，2.将坦克重新加入到窗口中
            MainGame.PI_TANK.display_tank()
            #v1.5调用我方坦克的移动方法
            if not MainGame.PI_TANK.stop:
                MainGame.PI_TANK.move()
            #刷新屏幕
            _display.update()
            #v1.5新增 主逻辑休眠
            # time.sleep(0.02)

    #事件处理方法
    def getEvent(self):
        #获取所有事件
        eventList = pygame.event.get()
        for event in eventList:
            #type属性
            if event.type == pygame.QUIT:
                print("退出游戏")
                self.gameOver()
            #判断事件类型如果为按键按下的时候，在进行具体点击哪个key的判断
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("向左移动")
                    #修改坦克的方向，因为坦克的图片取决于坦克的方向，修改方向意味着刷新时，坦克会换图片
                    MainGame.PI_TANK.direction = 'L'
                    #v1.5 新增，坦克移动的开关控制
                    MainGame.PI_TANK.stop = False
                    # MainGame.PI_TANK.move()
                elif event.key == pygame.K_RIGHT:
                    print("向右移动")
                    MainGame.PI_TANK.direction = 'R'
                    # MainGame.PI_TANK.move()
                    # v1.5 新增，坦克移动的开关控制
                    MainGame.PI_TANK.stop = False
                elif event.key == pygame.K_UP:
                    print("向上移动")
                    MainGame.PI_TANK.direction = 'U'
                    # MainGame.PI_TANK.move()
                    # v1.5 新增，坦克移动的开关控制
                    MainGame.PI_TANK.stop = False
                elif event.key == pygame.K_DOWN:
                    print("向下移动")
                    MainGame.PI_TANK.direction = 'D'
                    # MainGame.PI_TANK.move()
                    # v1.5 新增，坦克移动的开关控制
                    MainGame.PI_TANK.stop = False
                elif event.key == pygame.K_SPACE:
                    print("biu biu biu ~~")
            #v1.5 新增 按键松开事件处理
            if event.type == pygame.KEYUP:
                MainGame.PI_TANK.stop = True
    # 给一个字符串，返回一个包含字符串内容的表面(Surface)
    def drawText(self,content):
        #字体模块初始化
        pygame.font.init()
        #创建字体对象
        font = pygame.font.SysFont('kaiti',18)
        # fonts_list = pygame.font.get_fonts()
        # print(fonts_list)
        #kalinga
        #使用字体渲染内容 render()
        text_sf = font.render(content,True,COLOR_RED)
        #返回包含内容的Surface
        return text_sf
    def gameOver(self):
        exit()

#继承精灵类的类，供其他类来继承
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Tank(BaseItem):
    def __init__(self,left,top):
        #坦克图片集(上下左右四个方向)
        self.images = {
            #key为'U'  value:为 pygame.image.load('img/p1tankU.gif')得到的一个surface
            'U': pygame.image.load('img/p1tankU.gif'),
            'D': pygame.image.load('img/p1tankD.gif'),
            'L': pygame.image.load('img/p1tankL.gif'),
            'R': pygame.image.load('img/p1tankR.gif')
        }
        #坦克的方向
        self.direction = 'U'
        #坦克初始化时候的默认图片，根据坦克的方向从字典里去取
        self.image = self.images[self.direction]
        #坦克的区域(left,top,width,heigt) 坦克位置及坦克大小
        self.rect = self.image.get_rect()
        # 将坦克距左边的位置修改为参数指定的位置
        self.rect.left = left
        # 将坦克距上边的位置修改为参数指定的位置
        self.rect.top = top
        # 坦克的速度
        self.speed = 1
        #v1.5 新增 stop变量，用来控制坦克是否应该移动的开关
        self.stop = True

    #展示坦克
    def display_tank(self):
        #设置坦克图片
        self.image = self.images[self.direction]
        #将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)
    # v1.5 新增坦克移动方法
    def move(self):
        #修改tank的坐标：取决于坦克的方向
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT-MainGame.PI_TANK.rect.height:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH-MainGame.PI_TANK.rect.width:
                self.rect.left += self.speed

class MyTank(Tank):
    pass
class EnemyTank(Tank):
    pass
class Bullet(BaseItem):
    pass
class Explode():
    pass
class Musice():
    pass
game = MainGame()
game.startGame()