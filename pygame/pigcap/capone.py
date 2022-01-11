import pygame, sys, time, random

class Pig:
    '''
    position：列表，初始坐标
    id：整数，每头猪的编号
    field_size：列表或元组，战场的尺寸（长，高）
    '''

    count = 5000 #猪的数量
    speed = 1

    def __init__(self, position, id, field_size, field):
        '''
        初始化方法，定义基本属性
        position：列表，初始坐标
        id：整数，每头猪的编号
        field_size：列表或元组，战场的尺寸（长，高）
        '''
        self.position = position
        self.id = id 

        self.flag = False  #布尔值，猪被抓住的标志
        self.field_width = field_size[0]
        self.field_height = field_size[1]

        self.field = field
        self.field[position[0]][position[1]]=2 #在地图中将坐标值标记为2：猪类

    def capture(self):
        '''
        判断自己是否被抓，当 周围的人类>=3 就认为被抓住，并且修改count的值
        '''
        human_num=0 #循环周围的格子，检查有多少人类
        for i in range(-1,2):
            for j in range(-1,2):
                if 0<=self.position[0]+i < self.field_height and 0<=self.position[1]+j < self.field_width and self.field[self.position[0]+i][self.position[1]+j]==1:
                    human_num+=1
        #大于等于三个人就认为猪被抓住了
        if human_num>=3:
            Pig.count-=1
            self.flag=True
            print("%d号猪被抓" % self.id)

    def move(self):
        '''
        随机移动到新的地点，并修改自己的坐标
        '''
        #先判断周围是否有空位置可走，且未超过边界
        if((self.position[0]+1<self.field_height and self.field[self.position[0]+1][self.position[1]]==0) or\
            (self.position[0]-1>=0 and self.field[self.position[0]-1][self.position[1]]==0) or\
            (self.position[1]+1<self.field_width and self.field[self.position[0]][self.position[1]+1]==0) or\
            (self.position[1]-1>=0 and self.field[self.position[0]][self.position[1]-1]==0)):
            
            self.field[self.position[0]][self.position[1]]=0 #原来的位置改为0：空地

            while True:
                direction = random.randint(0,3) #0123，上下左右
                if direction == 0 and self.position[0]-1>=0 and self.field[self.position[0]-1][self.position[1]]==0: #如果向上有路可走
                    self.position[0] -= 1
                    break
                elif direction == 1 and self.position[0]+1<self.field_height and self.field[self.position[0]+1][self.position[1]]==0: #如果向下有路可走
                    self.position[0] += 1
                    break
                elif direction == 2 and self.position[1]-1>=0 and self.field[self.position[0]][self.position[1]-1]==0: #如果向左有路可走
                    self.position[1] -= 1
                    break
                elif direction == 3 and self.position[1]+1<self.field_width and self.field[self.position[0]][self.position[1]+1]==0: #如果向右有路可走
                    self.position[1] += 1
                    break

            self.field[self.position[0]][self.position[1]]=2#新的位置改为2：猪类

#人类
class Human:
    '''
    position：列表，初始坐标
    target：Pig对象，要抓的猪对象
    field_size：列表或元组，战场的尺寸（长，高）
    '''
    speed = 5
    def __init__(self, position, target, target_list, field_size, field):
        '''
        初始化方法，定义基本属性
        position：列表，初始坐标
        target：Pig对象，要抓的猪对象
        field_size：列表或元组，战场的尺寸（长，高）
        '''
        self.position = position
        self.target = target 
        self.target_list = target_list

        self.field_width = field_size[0]
        self.field_height = field_size[1]

        self.field = field
        self.field[position[0]][position[1]]=1 #在地图中将坐标值标记为1：人类

    def random_move(self):
        '''
        随机移动，并修改坐标
        '''
        while True:
            direction = random.randint(0, 3)#0123，上下左右
            if direction == 0 and self.position[0]-1>=0 and self.field[self.position[0]-1][self.position[1]]==0: #如果向上有路可走
                self.position[0]-=1
                break
            elif direction == 1 and self.position[0]+1<self.field_height and self.field[self.position[0]+1][self.position[1]]==0: #如果向下有路可走
                self.position[0]+=1
                break
            elif direction == 2 and self.position[1]-1>=0 and self.field[self.position[0]][self.position[1]-1]==0: #如果向左有路可走
                self.position[1]-=1
                break
            elif direction == 3 and self.position[1]+1<self.field_width and self.field[self.position[0]][self.position[1]+1]==0: #如果向右有路可走
                self.position[1]+=1
                break

    def move(self):
        '''
        沿着目标猪的方向移动到新的地点，并修改自己的坐标。
        '''
        self.field[self.position[0]][self.position[1]]=0#当前的位置改为0：空地

        #先判断周围是否有空位置可走，且未超过边界
        if((self.position[0]+1<self.field_height and self.field[self.position[0]+1][self.position[1]]==0) or\
            (self.position[0]-1>=0 and self.field[self.position[0]-1][self.position[1]]==0) or\
            (self.position[1]+1<self.field_width and self.field[self.position[0]][self.position[1]+1]==0) or\
            (self.position[1]-1>=0 and self.field[self.position[0]][self.position[1]-1]==0)):
            
            #如果有位置可走，随机01来确定先横走还是竖走，1是横走
            if random.randint(0,1):  

                if self.position[1]==self.target.position[1]: #如果随机到横走，判断是否已经在同一列，如果在就没必要横走，直接竖走
                    #纵坐标相减判断是向上(>0)还是向下(<0)走，且要判断是否可走
                    if self.position[0]-self.target.position[0] > 0 and self.field[self.position[0]-1][self.position[1]]==0:
                        self.position[0]-=1 #更改坐标

                    elif self.position[0]-self.target.position[0] < 0 and self.field[self.position[0]+1][self.position[1]]==0:
                        self.position[0]+=1
                    #竖向也没得走，随机走一步
                    else:
                        self.random_move()

                #如果不在同一列，横坐标相减判断是向左(>0)还是向右(<0)走，且要判断是否可走
                elif self.position[1]-self.target.position[1] > 0 and self.field[self.position[0]][self.position[1]-1]==0:
                    self.position[1]-=1

                elif self.position[1]-self.target.position[1] < 0 and self.field[self.position[0]][self.position[1]+1]==0 : 
                    self.position[1]+=1

                #横向没得走，转向竖走，一样抄的上面的
                else:
                    if self.position[0]-self.target.position[0] > 0 and self.field[self.position[0]-1][self.position[1]]==0:
                        self.position[0]-=1
                    #纵坐标相减判断是向下(>0)还是向上(<0)走，且要判断是否可走
                    elif self.position[0]-self.target.position[0] < 0 and self.field[self.position[0]+1][self.position[1]]==0:
                        self.position[0]+=1
                    else:
                        self.random_move()

            #----------------------------------------------------------------------------------------------
            #如果随机到竖走，以下逻辑全部同上，仅修改方向
            else:
                if self.position[0]==self.target.position[0]: #如果随机到竖走，判断是否已经在同一行，如果在就没必要竖走，直接横走
                    #横坐标相减判断是向左(>0)还是向右(<0)走，且要判断是否可走
                    if self.position[1]-self.target.position[1] > 0 and self.field[self.position[0]][self.position[1]-1]==0:
                        self.position[1]-=1

                    elif self.position[1]-self.target.position[1] < 0 and self.field[self.position[0]][self.position[1]+1]==0 : 
                        self.position[1]+=1
                    else:
                        self.random_move()

                #如果不在同一行，纵坐标相减判断是向上(>0)还是向下(<0)走，且要判断是否可走
                elif self.position[0]-self.target.position[0] > 0 and self.field[self.position[0]-1][self.position[1]]==0:
                    self.position[0]-=1
                #纵坐标相减判断是向上(>0)还是向下(<0)走，且要判断是否可走
                elif self.position[0]-self.target.position[0] < 0 and self.field[self.position[0]+1][self.position[1]]==0:
                    self.position[0]+=1

                #竖向没得走，转向横走
                else:
                    if self.position[1]-self.target.position[1] > 0 and self.field[self.position[0]][self.position[1]-1]==0:
                        self.position[1]-=1
                    #横坐标相减判断是向左(>0)还是向右(<0)走，且要判断是否可走
                    elif self.position[1]-self.target.position[1] < 0 and self.field[self.position[0]][self.position[1]+1]==0:
                        self.position[1]+=1
                    else:
                        self.random_move()

        #将新修改的位置改为1：人类
        self.field[self.position[0]][self.position[1]]=1

    def check_target(self):
        '''
        检查目标猪是否已被抓获，如果已被抓获则重新选择目标。
        '''
        if self.target.flag :   #如果目标猪的flag为True，那么更换目标
            if len(self.target_list):
                self.target=self.target_list[random.randint(0,len(self.target_list)-1)]#随机在pig_list里选一个
            else:
                print("猪抓完了")

class background(object):
    """docstring for background"""
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    # Goolge RGB
    blue = (66, 133, 244)
    red = (234, 67, 53)
    yellow = (251, 188, 5)
    green = (52, 168, 83)
    gray = (147, 147, 147)
    font = "freesansbold.ttf"

    def __init__(self, width, height, size):
        super(background, self).__init__()
        self.width = width
        self.height = height
        self.size = size 

        self.field_width = self.width//self.size
        self.field_height = self.height//self.size

        self.field_size = (self.field_width, self.field_height)
        self.field = [[0]*self.field_width for i in range(self.field_height)]

        

def main():

    width=1380  
    height=750
    size=5

    bg = background(width, height, size)    
    
    #程序窗口大小，初始化整个地图列表，因为渲染出来的人类和猪有尺寸，所以列表的范围是程序窗口大小除以尺寸
    #pygame的坐标系xy方向和二维列表的下标不一样，程序坐标均以列表为准，如[3,5] -> 第三行第五列 -> pygame x=5,y=3
    #pygame：0----->x
    #        |
    #        ↓
    #        y

    field_size = bg.field_size
    field = bg.field #0:空地，1:人类，2:猪  

    #初始化pygame，设置程序窗口和标题，窗口底部预留40像素的高度用来显示信息
    pygame.init()
    screen = pygame.display.set_mode((width, height+40))
    pygame.display.set_caption("Capture Pigs")
    #背景覆盖
    screen.fill(bg.white)

    #统一管理猪和人类的列表，方便批量操作

    def create_pigs(field, field_size, zone=(100, 50), left_up=(30, 60)):
        count = 0
        pig_list = []
        for i in range(zone[0]):
            for j in range(zone[1]):
                pig_list.append(Pig(position = [left_up[0] + 2*j, left_up[1] + 2*i], 
                                    id = i*zone[0] + j + 1, 
                                    field_size = field_size, 
                                    field = field))
                count += 1
        Pig.count = count
        return pig_list

    def create_human(field, field_size, target_list, zone=(20, 50), left_up=(20, 10)):
        human_list = []
        for i in range(zone[0]):
            for j in range(zone[1]):
                human_list.append(Human(position = [left_up[0] + 2*j, left_up[1] + 2*i], 
                                        target = target_list[random.randint(0, len(target_list)-1)], 
                                        target_list = target_list, 
                                        field_size = field_size, 
                                        field = field))
        return human_list

    # pig_list = create_pigs(field, field_size)
    # human_list = create_human(field, field_size, pig_list)
    
    Pig.speed = 1
    Human.speed = 5

    pig_list = create_pigs(field, field_size, zone=(10, 8), left_up=(100, 200))
    human_list = create_human(field, field_size, target_list=pig_list, zone=(10, 4), left_up=(20, 20))


    #画出刚刚创建的猪和人类
    target_line_color=pygame.Color(bg.yellow)
    human_color=pygame.Color(bg.blue)
    pig_color=pygame.Color(bg.red)

    for i in pig_list:
        #画布，颜色，矩形对象（坐标，尺寸），圆角半径
        pygame.draw.rect(screen, pig_color, pygame.Rect((i.position[1]*size, i.position[0]*size),(size,size)), border_radius=size//2)
    for i in human_list:
        pygame.draw.rect(screen, human_color, pygame.Rect((i.position[1]*size, i.position[0]*size),(size,size)), border_radius=size//2)

    pygame.display.update()  #更新屏幕

    frame=0#帧计数变量
    draw_target_line=False#是否绘制目标线，默认不绘制

    # cound down
    wait = 3
    i = 0
    while i < wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(bg.white)
        screen.blit(pygame.font.Font(bg.font, 22).render("{} seconds to start".format(wait-i), 1, bg.black),(300,300))
        pygame.display.update()
        time.sleep(1)
        i+=1

    #主循环
    #监听关闭事件和按键事件->时间计数+1 ->检查猪是否抓完->猪检查自己是否被抓，并删除已抓住的猪->人类检查目标状态并移动->猪移动->画出所有的猪和人
    while True:
        for event in pygame.event.get():  #监听事件
            if event.type == pygame.QUIT: #如果关闭窗口则退出程序
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == ord("q"):
                pygame.quit()
                sys.exit()
            # a键控制是否显示目标线
            if event.type == pygame.KEYDOWN and event.key == ord("a"):
                draw_target_line = not draw_target_line

        #背景覆盖
        screen.fill(bg.white)

        #时间计数+1，并绘制提示文字
        frame+=1
        screen.blit(pygame.font.Font(bg.font, 24).render("time (m): {}".format(frame*4), 1, bg.green), (250,2))
        screen.blit(pygame.font.Font(bg.font, 24).render("pigs left: {}".format(Pig.count), 1, bg.yellow),(500,2))
        screen.blit(pygame.font.Font(bg.font, 22).render("blue: human beings", 1, human_color), (700,2))
        screen.blit(pygame.font.Font(bg.font, 22).render("red: pigs", 1, pig_color), (950,2))
        screen.blit(pygame.font.Font(bg.font, 15).render("press Q to quit", 1, bg.gray), (1100,8))

        #检查猪抓完没有，并绘制猪数量的提示文字
        if not len(pig_list):
            screen.blit(pygame.font.Font(bg.font,50).render("mission completed in %d hours"%(frame*4//60), 1, bg.black),(300,300))
            pygame.display.update()
            print(frame*4)
            time.sleep(6)
            pygame.quit()
            sys.exit()

        #绘制是否开启目标线的提示文字
        if draw_target_line:
            screen.blit(pygame.font.Font(bg.font,22).render("press A for target line: on", 1, bg.yellow),(600,750))
        else:
            screen.blit(pygame.font.Font(bg.font,22).render("press A for target line: off", 1, bg.gray),(600,750))

        #开始抓猪
        #把已经被抓住的猪从列表里删除
        for i in pig_list:
            i.capture()
            if i.flag:
                pig_list.remove(i)

        #所有人类检查自己的目标是否存活，并移动一步，画出对应猪和目标的提示线
        for i in human_list:
            i.check_target()
            i.move()
            if draw_target_line:
                pygame.draw.aaline(screen, target_line_color, (i.position[1]*size+size//2,i.position[0]*size+size//2), (i.target.position[1]*size+size//2,i.target.position[0]*size+size//2), 1)

        #计算人类和猪的移速比，时间到了所有的猪移动一步
        if frame%(Human.speed//Pig.speed + 1)==0:
            for i in pig_list:
                i.move()

        #画出所有的人类和猪
        for i in human_list:
            pygame.draw.rect(screen, human_color,pygame.Rect((i.position[1]*size,i.position[0]*size),(size,size)),border_radius=size//2)
        for i in pig_list:
            pygame.draw.rect(screen, pig_color,pygame.Rect((i.position[1]*size,i.position[0]*size),(size,size)),border_radius=size//2)


        #更新屏幕
        pygame.display.update()
        #运行速度
        pygame.time.Clock().tick(60)
    return None



if __name__ == '__main__':
    main()