#测试一下
#Location （位置）喝醉的的人现在在哪儿
#CompassPt （方向）被称为罗经点的数据抽象来代表，这个人会朝 n北 s南 e东 w西四个方向走
#Field （场地）很明显的是这个人在这个场地中，因此我也想把场地当做一个独立的事物（笛卡尔平面）
#Drunk 最后 我最好喝点酒



import math, random, pylab

class Location(object):   #位置（笛卡尔平面中的一个点）
    def __init__(self, x, y):  #返回一个 x坐标  y坐标的点
        self.x = float(x)
        self.y = float(y)
    def move(self, xc, yc):   #用move来模拟这个人走一步
        return Location(self.x+float(xc), self.y+float(yc))    #给一个x坐标 y坐标变化的点，然后它会返回一个新的点的位置
    def getCoords(self):     #返回一个 x坐标  y坐标的点
        return self.x, self.y
    def getDist(self, other):  #通过求直角三角形的斜边，来算一个点离原点有多远
        ox, oy = other.getCoords()
        xDist = self.x - ox
        yDist = self.y - oy
        return math.sqrt(xDist**2 + yDist**2)

class CompassPt(object):
    possibles = ('N', 'S', 'E', 'W')
    def __init__(self, pt):
        if pt in self.possibles: self.pt = pt   #self.possibles指 CompassPt这个类
        else: raise ValueError('in CompassPt.__init__')  #在Python中，要想引发异常，最简单的形式就是输入关键字raise，后跟要引发的异常的名称。
    def move(self, dist):
        if self.pt == 'N': return (0, dist)
        if self.pt == 'S': return (0, -dist)
        if self.pt == 'E': return (dist, 0)
        if self.pt == 'W': return (-dist, 0)
        else: raise ValueError('in CompassPt.move')

class Field(object):
    def __init__(self, drunk, loc):   #loc 位置
        self.drunk = drunk
        self.loc = loc
    def move(self, cp, dist):
        oldLoc = self.loc        #原来的位置Location
        xc, yc = cp.move(dist)   #程序会调用CompassPt中的move方法，因为后面（Drunk类中）会看到cp是类CompassPt的对象
        self.loc = oldLoc.move(xc, yc)  #程序会调用Location类中的move方法，这个操作会让x y 加上合适的值,然后知道醉汉新的位置
    def getLoc(self):
        return self.loc    #返回这个喝醉的人的位置
    def getDrunk(self):
        return self.drunk

class Drunk(object):
    def __init__(self, name):
        self.name = name
    def move(self, field, time = 1):  #这里封装了醉酒者实际要做的一些决定，time醉酒者要移动多久
        if field.getDrunk() != self:  #如果你要求我对一个drunk进行move的操作，如果这个对象不在Field类内，这就没意义了
            raise ValueError('Drunk.move called with drunk not in field')
        for i in range(time):
            pt = CompassPt(random.choice(CompassPt.possibles))   #random.choice(sequence)从序列中获取一个随机元素。pt=CompassPt（E/S/W/N）
            field.move(pt, 1)
            

def performTrial(time, f):
    start = f.getLoc()    #得到一个起点，无论这个喝醉的人现在在场地的那个位置
    distances = [0.0]
    for t in range(1, time + 1):
        f.getDrunk().move(f)   #先调用Field.getDrunk方法，返回当前field中的drunk类的对象。然后再去调用Drunk.move方法(后面程序组合部分有定义drunk = Drunk('Homer Simpson'))，对这个对象进行移动，
        newLoc = f.getLoc()     #新地点
        distance = newLoc.getDist(start)  #位移后的位置离起点有多远
        distances.append(distance)
    return distances   #数组里面存放了每步过后这个醉酒者距离起点的距离
            

drunk = Drunk('Homer Simpson')
for i in range(3):    #进行3次不同的模拟
    f = Field(drunk, Location(0, 0))   #从场地的中间开始
    distances = performTrial(500, f)  #在这个场地上走500步
    pylab.plot(distances)
pylab.title('Homer\'s Random Walk')
pylab.xlabel('Time')
pylab.ylabel('Distance from Origin')

##pylab.show()

def performSim(time, numTrials):   #可以传入time和想要尝试的次数
    distLists = []
    for trial in range(numTrials):
        d = Drunk('Drunk' + str(trial))
        f = Field(d, Location(0, 0))
        distances = performTrial(time, f)
        distLists.append(distances)
    return distLists

        
        
