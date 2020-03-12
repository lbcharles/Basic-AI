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
       self.__x =1
       self.__y =1
       #dis: 0->right 1->down 2->left 3->up
       self.__dir =0
       self.__visited =set([(1,1)])
       self.__safe =set([(1,1)])
       self.__col = 0
       self.__row = 0
       #all property
       #' '->nothing in the room 'B'->breeze 'S'->stench 'W'->wupus 'G'->gold 'P'->pit 'U'->unknown 
       self.__property=defaultdict(set) #ex: {(1,1):{'P','S',' '}}
       self.__potential_pit=set()
       self.__potential_wupus =set()
       self.__breeze =set()
       self.__stench =set()
       self.__wupus=[]
       self.__pit=set()
       self.__frontier=[]

       self.__shoot = False
       self.__hasShoot = True

       self.__leave=False
       self.__action =[]
       self.__move=[]

    def set(self,set1,x,y,z):
        self.__x=x
        self.__y=y
        self.__dir=z
        self.__safe = set1

    def cal_cost(self,pairs_a,pairs_b,a_dir):
        #left
        score=0
        #b is at left of a
        if pairs_a[1] - pairs_b[1] > 0:
            if a_dir == 0:
                score+=2
            elif a_dir ==3 or a_dir ==1:
                score+=1
        #right
        elif pairs_b[1] - pairs_a[1] >0:
            if a_dir ==2:
                score+=2
            elif a_dir ==3 or a_dir ==1:
                score+=1
        #down
        if pairs_a[0] - pairs_b[0] >0:
            if a_dir ==3:
                score+=2
            elif a_dir ==2 or a_dir==0:
                score+=1
        #up
        elif pairs_b[0] - pairs_a[0]>0:
            if a_dir ==1:
                score+=2
            elif a_dir ==2 or a_dir==0:
                score+=1
        score+=abs(pairs_a[0]-pairs_b[0])
        score+=abs(pairs_a[1]-pairs_b[1])
        return score

    #sort a list by the distance between curretn pairs and target pairs
    def sort_list(self,l,pairs,curr_dir):
        for i in range(len(l)):
            l[i] = (l[i], self.cal_cost(pairs,l[i],curr_dir))
        sort= sorted(l,key= lambda x:(x[1],x[0]))
        return [j[0] for j in sort]        


    def update_frontier(self):
        for i in self.get_neighbor((self.__x,self.__y)):
            if i not in self.__potential_pit and i not in self.__potential_wupus and i not in self.__wupus and i not in self.__visited:
                self.__frontier.append(i)
                self.__safe.add(i)
        self.__frontier = list(set(self.__frontier))
        self.__frontier = self.sort_list(self.__frontier,(self.__x,self.__y),self.__dir)


    #turn left or right
    def fix_dir(self,left,right):
        if self.__dir ==0:
            if left ==True:
                self.__dir =3
            else:
                self.__dir =1
        elif self.__dir ==2:
            if left==True:
                self.__dir=1
            else:
                self.__dir=3
        elif self.__dir ==3:
            if left ==True:
                self.__dir=2
            else:
                self.__dir=0
        elif self.__dir==1:
            if left==True:
                self.__dir=0
            else:
                self.__dir=2

    def get_neighbor(self,pairs):
        neighbor = []
        if pairs[1]-1 >0:
            neighbor.append( (pairs[0],pairs[1]-1) )
        if pairs[0]-1 >0:
            neighbor.append( (pairs[0]-1,pairs[1]) )
        if (self.__row!=0 and pairs[0]+1 <= self.__row) or self.__row==0:
            neighbor.append( (pairs[0]+1,pairs[1]) )
        if (self.__col!=0 and pairs[1]+1 <= self.__col) or self.__col ==0:
            neighbor.append( (pairs[0],pairs[1]+1) )
        return neighbor

    #update potential pit and wupus
    def judge(self):
        r_item =[]
        for i in self.__potential_pit:
            if i in self.__property and 'P' not in self.__property[i]:
                r_item.append(i)
            else:
                for j in self.get_neighbor(i):
                    if j in self.__property and 'B' not in self.__property[j]:
                        r_item.append(i)
                        break
        for r in r_item:
            self.__potential_pit.discard(r)
            if r not in self.__visited and r not in self.__potential_wupus and r not in self.__wupus:
                self.__frontier.append(r)
        r_list=[]
        for k in self.__potential_wupus:
            if k in self.__property and 'W' not in self.__property[k]:
                r_list.append(k)
            else:
                for h in self.get_neighbor(k):
                    if h in self.__property and 'S' not in self.__property[h]:
                        r_list.append(k)
                        break
        for l in r_list:
            self.__potential_wupus.discard(l)
            if l not in self.__visited and l not in self.__potential_pit and l not in self.__wupus:
                self.__frontier.append(l)

    
    #calcute the room of wupus
    def find_wupus(self):
        if self.__wupus or "died" in self.__wupus:
            return
        else:
            if len(self.__stench) >=2:
                stench=list(self.__stench)
                stench_l =[]
                #crosswise
                #if len>2 , there must appare crosswise
                for i in stench:
                    for j in stench:
                        if i!=j and i[0] == j[0]:
                            self.__wupus.append( (i[0],(i[1]+j[1])/2) )
                            break
                        elif i!=j and i[1] == j[1]:
                            self.__wupus.append( ((i[0]+j[0])/2,i[1]) )
                            break
                #diagonally
                #if len=2, may appear
                if len(self.__stench) ==2:
                    if abs(stench[0][0]-stench[1][0])==1 and abs(stench[0][1] - stench[1][1]) ==1:
                        check_l=[ (stench[0][0],stench[1][1]) ,(stench[1][0],stench[0][1]) ]
                        if check_l[0] in self.__property and self.__property[check_l[0]] != 'W':
                            self.__wupus.append(check_l[1])
                        if check_l[1] in self.__property and self.__property[check_l[1]] != 'W':
                            self.__wupus.append(check_l[0])
        if self.__wupus:
            self.__potential_wupus=set()
        return self.__wupus


    def update_property(self,pairs):
        if 'B' in self.__property[pairs]:
            self.__breeze.add(pairs)
            self.__safe.add(pairs)
            #pit may appear in any of the neighbors of B
            self.__potential_pit.update(self.get_neighbor(pairs))

        if 'S' in self.__property[pairs]:
            self.__stench.add(pairs)
            self.__safe.add(pairs)
            #wupus may appear in any of the neighbors of S
            if not self.__wupus or "died" not in self.__wupus:
                self.__potential_wupus.update(set(self.get_neighbor(pairs)))

        if 'G' in self.__property[pairs]:
            self.__safe.add(pairs)
        if ' ' in self.__property[pairs]:
            self.__safe.add(pairs)
        #judge position of pit and wupus
        self.judge()
        self.find_wupus()


    #
    def veer(self,curr,target):
        left_l=[(1,0),(2,1),(3,2),(0,3)]
        action=[]
        if curr == target:
            return action
        if abs(curr-target) ==2:
            action.extend(["Agent.Action.TURN_LEFT","Agent.Action.TURN_LEFT"])
            return action
        if (curr,target) in left_l:
            action.append("Agent.Action.TURN_LEFT")
        else:
            action.append("Agent.Action.TURN_RIGHT")
        return action


    def relative_position(self,pairs_a,pairs_b):
        # relation between 2 pairs
        # 0 ->right   1->down    2->right    3->up   4->b not related to a
        if pairs_b[0] == pairs_a[0] and pairs_b[1] == pairs_a[1]+1:
            return 0
        elif pairs_b[0] == pairs_a[0]-1 and pairs_b[1] == pairs_a[1]:
            return 1
        elif pairs_b[0] == pairs_a[0] and pairs_b[1] == pairs_a[1]-1:
            return 2
        elif pairs_b[0] == pairs_a[0] +1 and pairs_b[1] == pairs_a[1]:
            return 3
        else:
            return 4

    def path(self,curr,cur_dir,target):
        q=[(curr,cur_dir)]
        duplicated = set(q[0])
        path = dict()
        min_cost =0
        l_path =[]
        while q:
            first_pairs = q[0]
            q.pop(0)
            neighbor = self.get_neighbor(first_pairs[0])
            neighbor= self.sort_list(neighbor,first_pairs[0],first_pairs[1])
            for i in neighbor:
                if i not in duplicated and i in self.__safe:
                    path[i] = first_pairs[0]
                    if i !=target:
                        duplicated.add(i)
                        q.append((i,self.relative_position(first_pairs[0],i)))
                    else:
                        list1= self.escapeRoute(i,curr,path,[])
                        if self.cost(curr,cur_dir,list1,0) < min_cost or min_cost ==0:
                            min_cost = self.cost(curr,cur_dir,list1,0)
                            l_path=list1
        return l_path

    def escapeRoute(self,target,curr,path:dict,list1:list):
        if target == curr:
            return list1
        else:
            list1.insert(0,target)
            return self.escapeRoute(path[target],curr,path,list1)

    def cost(self,curr,c_dir,pathL:list,score):
        curr_dir= c_dir
        if self.relative_position(curr,pathL[0]) == curr_dir:
            score+=1
        elif abs(curr_dir - self.relative_position(curr,pathL[0])) ==2:
            score+=3
            curr_dir = self.relative_position(curr,pathL[0])
        else:
            score+=2
            curr_dir= self.relative_position(curr,pathL[0])
        if len(pathL) ==1:
            return score
        return self.cost(pathL[0],c_dir,pathL[1:],score)

    def escapeAction(self,curr,c_dir,target_dir,list1:list):
        action=[]
        while list1:
            action.extend(self.veer(c_dir,self.relative_position(curr,list1[0])))
            action.append("Agent.Action.FORWARD")
            c_dir = self.relative_position(curr,list1[0])
            curr = list1[0]
            list1.pop(0)
        if target_dir != None:
            action.extend(self.veer(c_dir,target_dir))

        return action


    #update dir and (x,y) when using return with eval
    def update(self,action):
        if action == "Agent.Action.FORWARD":
            if self.__dir == 0:
                self.__y +=1
            elif self.__dir ==1:
                self.__x -=1
            elif self.__dir ==2:
                self.__y -=1
            elif self.__dir ==3:
                self.__x+=1
        elif action == "Agent.Action.TURN_LEFT":
            self.fix_dir(True,False)
        elif action == "Agent.Action.TURN_RIGHT":
            self.fix_dir(False,True)

    def move_action(self,action,move):
        if action:
            action=self.__action.pop(0)
            self.update(action)
            return eval(action)
        else:
            action = self.__move.pop(0)
            self.update(action)
            return eval(action)


    def out_range(self):
        l1=list(self.__potential_pit)
        for i in l1:
            if i [0] > self.__row and self.__row!=0:
                l1.remove(i)
            if i[1]> self.__col and self.__col !=0:
                l1.remove(i)
        self.__potential_pit = set(l1)
        l2=list(self.__potential_wupus)
        for j in l2:
            if j[0] > self.__row and self.__row!=0:
                l2.remove(j)
            if j[1] > self.__col and self.__col !=0:
                l2.remove(j)
        self.__potential_wupus = set(l2)
        l3 = list(self.__visited)
        for h in l3:
            if h[0] > self.__row and self.__row!=0:
                l3.remove(h)
            if h[1] > self.__col and self.__col !=0:
                l3.remove(h)
        self.__visited = set(l3)
        l4 = list(self.__safe)
        for k in l4:
            if k[0] >self.__row and self.__row!=0:
                l4.remove(k)
            if k[1] >self.__col and self.__col!=0:
                l4.remove(k)
        self.__safe = set(l4)


    def getAction( self, stench, breeze, glitter, bump, scream ):
        if bump:
            if self.__dir == 0: #right
                self.__col=self.__y-1
                self.__y-=1
            elif self.__dir == 3:#up
                self.__row=self.__x-1
                self.__x -=1
            self.out_range()
        if glitter:
            self.__property[(self.__x,self.__y)].add('G')
            self.update_property( (self.__x,self.__y) )
            self.__visited.add((self.__x,self.__y))
            self.__leave =True
            return Agent.Action.GRAB
        if stench:
            self.__property[(self.__x,self.__y)].add('S')
            #self.update_property( (self.__x,self.__y) )
        if breeze:
            if self.__x==1 and self.__y==1:
                return Agent.Action.CLIMB
            self.__property[(self.__x,self.__y)].add('B')
        self.update_property( (self.__x,self.__y) )
        if scream:
            if self.__wupus:
                if self.__wupus[0] not in self.__potential_pit:
                    self.__safe.add(self.__wupus[0])
                    self.__frontier.append(self.__wupus[0])
                    self.__frontier = self.sort_list(self.__frontier,(self.__x,self.__y),self.__dir)
            else:
                self.__wupus = ["died"]
                self.__property[(self.__x,self.__y)].discard('S')

        self.__property[(self.__x,self.__y)].add(' ')
        self.update_property( (self.__x,self.__y) )
        self.__visited.add((self.__x,self.__y))

        self.update_frontier()

        if self.__x==1 and self.__y==1 and 'S' in self.__property[(self.__x,self.__y)] and self.__hasShoot:
            self.__hasShoot = False
            return Agent.Action.SHOOT

        if self.__action and not self.__leave:
            return self.move_action(True,False)

        if self.__move and not self.__leave:
            return self.move_action(False,True)

        if self.__wupus and self.__hasShoot and not self.__leave and (self.__x == self.__wupus[0][0] or self.__y == self.__wupus[0][1]):
            self.__shoot = True
            self.__hasShoot = False
            self.__action=self.veer(self.__dir,self.relative_position((self.__x,self.__y), self.__wupus[0]))
            if self.__action:
                return self.move_action(True,False)

        if self.__wupus and self.__shoot and not self.__leave and self.relative_position((self.__x,self.__y), self.__wupus[0]) == self.__dir:
            self.__shoot= False
            return Agent.Action.SHOOT

        if self.__frontier and not self.__leave:
            target = self.__frontier.pop(0)
            self.__visited.add(target)
            list1 = self.path((self.__x,self.__y),self.__dir,target )
            path_to_t=self.escapeAction((self.__x,self.__y),self.__dir,None, list1)
            self.__move = path_to_t
            return self.move_action(False,True)
        elif not self.__frontier or self.__leave:
            target = (1,1)
            list1 = self.path((self.__x,self.__y),self.__dir,target)
            path_to_t = self.escapeAction( (self.__x,self.__y),self.__dir, None, list1)
            self.__move = path_to_t
            self.__move.append("Agent.Action.CLIMB")
            return self.move_action(False,True)
