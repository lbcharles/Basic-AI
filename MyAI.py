# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import defaultdict

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.__x = 1
        self.__y = 1
        #dir: 0 -> right 1 -> down  2 -> left  3 -> up
        self.__dir = 0
        self.__visited = defaultdict(str)
        self.__frontier = {}
        self.__wumpus = []
        self.__wumpus_exist = True
        self.__pit= set()
        self.__which_dir= 0
        self.__return = False
        self.__navigation = [0,0] #[dir,step]
        self.__aim = [0,0]
        self.__potential_danger = set()
        self.__neighbor = set()
        self.__shoot = False
        self.__have_shot = False
        self.__width = 1000
        self.__length = 1000
        self.__trace_back = False
        self.__aim_neighbor = set()
        self.__have_grab = False
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.__neighbor = self.get_neighbor(self.__x,self.__y)
        print(self.__neighbor)

        if scream:
            self.__wumpus_exist = False
            self.__wumpus.pop(0)

        if self.__x == 1 and self.__y== 1:
            if breeze:
                return Agent.Action.CLIMB
            if stench:
                if self.__have_shot == False:
                    self.__wumpus.append((2,1))
                    self.__wumpus.append((1,2))
                    self.__have_shot = True
                    return Agent.Action.SHOOT
                if self.__wumpus_exist == True and self.__have_shot == True:
                    try:
                        self.__wumpus.remove((1,2))
                    except:
                        pass

        if self.__shoot == True and self.__have_shot == False:
            self.__shoot = False
            self.__have_shot = True
            return Agent.Action.SHOOT

        if (self.__x,self.__y) not in self.__visited:
            if breeze:
                self.__visited[(self.__x,self.__y)] += "b"
                self.update_danger()
            if stench and self.__wumpus_exist == True and len(self.__wumpus) == 0:
                self.__visited[(self.__x,self.__y)] += "s"
                self.update_danger()
                if self.__have_shot == True and (self.__x, self.__y) == (1,1):
                    self.__potential_danger.remove((1,2))
            if glitter:
                self.__visited[(self.__x,self.__y)] += "g"
                self.__return = True
                self.__have_grab = True
                return Agent.Action.GRAB
            self.__visited[(self.__x,self.__y)] += ""

        print(self.__potential_danger)
        for i in self.__neighbor:
            if i in self.__potential_danger:
                self.analyze(i)
            if i not in self.__visited and i not in self.__potential_danger and i not in self.__pit and i not in self.__wumpus:
                self.__frontier[i] = ""

        if len(self.__frontier) == 0:
            self.__return = True

        if self.__have_grab == True:
            self.__return = True

        if self.__return == True and (self.__x,self.__y) == (1,1):
            return Agent.Action.CLIMB

        print(self.__potential_danger)



        if self.__shoot == True and self.__have_shot == False:
            print("sssss")
            self.__aim = self.__wumpus[0]
            print("qweweqwewqe : ",self.__aim)
            self.__frontier[self.__wumpus[0]] = ""
            if self.__x - self.__aim[0] > 0:
                self.__which_dir = 1
            elif self.__x - self.__aim[0] < 0:
                self.__which_dir = 3
            elif self.__y - self.__aim[1] > 0:
                self.__which_dir = 2
            elif self.__y - self.__aim[1] < 0:
                self.__which_dir = 0
            num2 = self.__which_dir - self.__dir
            print("num2: ", num2)
            if num2 == 3:
                self.__dir += 3
                print("OK")
                return Agent.Action.TURN_LEFT
            elif num2 == 1:
                self.__dir += 1
                print("OK")
                return Agent.Action.TURN_RIGHT
            elif num2 == -3:
                self.__dir -= 3
                print("OK")
                return Agent.Action.TURN_RIGHT
            elif num2 == -1:
                self.__dir -=1
                print("OK")
                return Agent.Action.TURN_LEFT
            elif num2 == 0:
                self.__shoot = False
                self.__have_shot = True
                return Agent.Action.SHOOT
        
        if bump:
            del self.__visited[(self.__x,self.__y)]
            if self.__dir == 0:
                if (self.__x,self.__y+1) in self.__frontier:
                    del self.__frontier[(self.__x,self.__y+1)]
                if (self.__x+1,self.__y) in self.__frontier:
                    del self.__frontier[(self.__x+1,self.__y)]
                if (self.__x-1,self.__y) in self.__frontier:
                    del self.__frontier[(self.__x-1,self.__y)]
                self.__y -= 1
                self.__length = self.__y
            elif self.__dir == 3:
                if (self.__x+1,self.__y) in self.__frontier:
                    del self.__frontier[(self.__x+1,self.__y)]
                if (self.__x,self.__y-1) in self.__frontier:
                    del self.__frontier[(self.__x,self.__y-1)]
                if (self.__x,self.__y+1) in self.__frontier:
                    del self.__frontier[(self.__x,self.__y+1)]
                self.__x -= 1
                self.__width = self.__x
                #self.__aim = pq[0]
        pq = sorted(self.__frontier.keys(),key = lambda x:(x[0],x[1]))
        
        if len(pq) > 0:
            self.__aim = pq[0]
        else:
            self.__return = True

        if self.__return == True:
            self.__aim = [1,1]

        print(self.__wumpus)
        print(self.__pit)
    
        navi2 = self.get_navigation()
        print(navi2)
        if self.__trace_back == True:
            print("__trace_back")
            #neighb = self.get_neighbor(self.__x,self.__y)
            # n_l = set()
            # print("neighb : ",neighb)
            # for i in neighb:
            #     if i in (set(self.__wumpus) | self.__potential_danger |self.__pit ):
            #         n_l.add(i)
            #     if i not in self.__visited:
            #         n_l.add(i)
            # for j in n_l:
            #     neighb.remove(j)
            # print("n_l : ",n_l)
            # print("neighb : ",neighb)
            aim_neighbor = self.get_neighbor(self.__aim[0], self.__aim[1])
            print(aim_neighbor)
            n_l = set()
            for i in aim_neighbor:
                if i in (set(self.__wumpus) | self.__potential_danger |self.__pit ):
                     n_l.add(i)
                if i not in self.__visited:
                    n_l.add(i)
            for j in n_l:
                aim_neighbor.remove(j)

            for k in aim_neighbor:
                if i[0]-self.__x == 0 or i[1]-self.__y == 0:
                    continue
                else:
                    self.__aim = k

            self.__frontier[self.__aim] = ""
            print(self.__aim)

            self.__aim_neighbor.update(aim_neighbor)
            if (self.__x,self.__y) in self.__aim_neighbor:
                self.__trace_back = False

            # coor = self.get_nearest(neighb)
            # self.__frontier[coor] = ""

            # if self.__dir == 3:
            #     self.__frontier[(self.__x-1,self.__y)] = ""
            #     print("trace back")
            #     self.__aim = [self.__x-1,self.__y]
            # elif self.__dir == 2:
            #     self.__frontier[(self.__x,self.__y+1)] = ""
            #     self.__aim = [self.__x,self.__y+1]
            #     print("trace back")
            # elif self.__dir == 1:
            #     self.__frontier[(self.__x+1,self.__y)] = ""
            #     self.__aim = [self.__x+1,self.__y]
            #     print("trace back")
            # elif self.__dir == 0:
            #     self.__frontier[(self.__x,self.__y-1)] = ""
            #     self.__aim = [self.__x,self.__y-1]
            #     print("trace back")
        # pq = sorted(self.__frontier.keys(),key = lambda x:(x[0],x[1]))
        # self.__aim = pq[0]
        navi2 = self.get_navigation()

        print(self.__frontier)
        print(pq)
        print(self.__aim)
        print(navi2)
        
        self.__which_dir = navi2[0]
        if self.__which_dir == self.__dir:
            self.forward()
            print((self.__x,self.__y))
            if (self.__x,self.__y) in self.__frontier:
                del self.__frontier[(self.__x,self.__y)]
            return Agent.Action.FORWARD
        else:
            num3 = self.__which_dir - self.__dir
            if num3 == 3:
                self.__dir += 3
                return Agent.Action.TURN_LEFT
            elif num3 == 1:
                self.__dir += 1
                return Agent.Action.TURN_RIGHT
            elif num3 == -3:
                self.__dir -= 3
                return Agent.Action.TURN_RIGHT
            elif num3 == -1:
                self.__dir -=1
                return Agent.Action.TURN_LEFT
            else:
                if self.__dir == 3:
                    self.__dir = 0
                else:
                    self.__dir += 1
                return Agent.Action.TURN_RIGHT
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def get_neighbor(self,x,y):
        neighbor=set()
        if y-1 > 0:
            neighbor.add( (x,y-1) )
        if x-1 > 0:
            neighbor.add( (x-1,y) )
        if y+1 <= self.__length:
            neighbor.add((x,y+1))
        if x+1 <= self.__width:
            neighbor.add((x+1,y))
        return neighbor

    def get_navigation(self): 
        stepc = self.__x - self.__aim[0]
        stepr = self.__y - self.__aim[1]
        navi = []
        if self.__trace_back == True:
            print("back trace ")
            if stepc < 0:
                navi =  [3,abs(stepc)]
            elif stepc > 0:
                navi = [1,abs(stepc)]
            elif stepr < 0:
                navi =  [0,abs(stepr)]
            elif stepr > 0:
                navi =  [2,abs(stepr)]
        if (self.__x, self.__y+1) not in (set(self.__wumpus) | self.__potential_danger |self.__pit ) :
            if stepr < 0:
                navi =  [0,abs(stepr)]
        if (self.__x, self.__y-1) not in ( set(self.__wumpus) | self.__potential_danger |self.__pit ):
            if stepr > 0:
                navi =  [2,abs(stepr)]
        if (self.__x+1, self.__y) not in (set(self.__wumpus) | self.__potential_danger |self.__pit ):
            if stepc < 0:
                navi =  [3,abs(stepc)]
        if (self.__x-1, self.__y) not in ( set(self.__wumpus) | self.__potential_danger |self.__pit ):
            if stepc > 0:
                navi = [1,abs(stepc)]
        if navi == []:
            self.__trace_back = True
        return navi

    def analyze(self, coordinate):
        neighbor = self.get_neighbor(coordinate[0],coordinate[1])
        b = 0
        s = 0
        known = 0
        for i in neighbor:
            if i in self.__visited:
                known += 1
                if "b" in self.__visited[i]:
                    b += 1
                if "s" in self.__visited[i]:
                    s += 1
        print("known = ",known)
        print("b = ",b)
        print("s = ",s)
        if b > 1 and b == known:
            self.__pit.add(coordinate)
            self.__potential_danger.discard(coordinate)

        if s > 1 and s == known:
            if self.__wumpus_exist:
                self.__wumpus.append(coordinate)
            print("wumpus at", coordinate)
            if coordinate not in self.__pit:
                if self.__wumpus_exist:
                    self.__potential_danger.discard(coordinate)
                    print("wumpus at", coordinate)
                    self.__shoot = True

        if b != known and s != known:
            self.__potential_danger.discard(coordinate)

    def forward(self):
        if self.__dir == 0:
            self.__y += 1
        elif self.__dir == 1:
            self.__x -= 1
        elif self.__dir == 2:
            self.__y -= 1
        elif self.__dir == 3:
            self.__x += 1

    def find_nearest(self, pq):
        r = 1000
        a = [0,0]
        for i in pq:
            n = abs(i[0]-self.__x) + abs(i[1]-self.__y)
            if n < r:
                a = i
                r = n
        return a

    def update_danger(self):
        neighbor = self.get_neighbor(self.__x,self.__y)
        for i in neighbor:
            if i not in self.__visited:
                self.__potential_danger.add(i)

    def get_nearest(self, neighbor):
        l = 1000
        c = (1,1)
        for i in neighbor:
            s = abs(i[0]-self.__aim[0]) + abs(i[1]-self.__aim[1])
            if i[0]-self.__aim[0] == 0 or i[1]-self.__aim[1] == 0:
                s += 1
            if s < l:
                l = s
                c = i
        return c


            
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
