class Frontier():

    def __init__(self):
        self.frontier=[]

    def insert(self,node):

        self.frontier.append(node)
        self.frontier.sort(key= lambda element: element.state[1])

    def isEmpty(self):
        return len(self.frontier) == 0

    def pop(self):
        if len(self.frontier)==0:
            raise Exception('error')
        elif len(self.frontier)==1:
            a= self.frontier[0]
            self.frontier=[]
            return a
        else:
            a=self.frontier[0]
            self.frontier=self.frontier[1:]
            return a

    def containsState(self,state):
        return any(node.state==state for node in self.frontier)

    def printf(self):
        list=[]
        for node in self.frontier:
            list.append(node.state)
        print(list)


class Node():

    def __init__(self,state,cost,parent,action):
        self.state=(state,cost)
        self.parent=parent
        self.action=action

class Map():

    def __init__(self,filename):

        with open(filename) as f:
            content=f.read()
        self.contents=content.splitlines()

        self.height=len(self.contents)
        self.width=max(len(line) for line in self.contents)

        self.road=[[False for num in range(self.width)] for num in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):

                if self.contents[i][j]=='-':
                    self.road[i][j]=True
                if self.contents[i][j].isalpha()==True:
                    self.road[i][j]=True
                if self.contents[i][j]=='a':
                    self.root=(i,j)
                if self.contents[i][j]=='c':
                    self.goal=(i,j)

    def findChild(self,state):

        ((i,j),cost)=state
        actions = [
            ('north',((i-1,j),cost+1)),
            ('south',((i+1,j),cost+1)),
            ('west',((i,j-1),cost+1)),
            ('east',((i,j+1),cost+1)),
            ('north-east',((i-1,j+1),cost+1)),
            ('north-west',((i-1,j-1),cost+1)),
            ('south-west',((i+1,j-1),cost+1)),
            ('south-east',((i+1,j+1),cost+1))
             ]
        self.content=[]
        for line in self.contents:
            self.content.append(list(self.contents))

        result=[]
        for action, ((r,c), costing) in actions:

            if 0<=r<self.height and 0<=c<self.width and self.road[r][c]==True:
                self.road[r][c]='path'
                result.append((action,((r,c),costing)))
        return result
    def solve(self):
        self.state_explored=0
        start= Node(state=self.root,cost=0,parent=None,action=None)
        frontier = Frontier()
        frontier.insert(start)

        self.explored=set()
        while True:

            if frontier.isEmpty()==True:
                raise Exception('no solution')

            node=frontier.pop()
            self.state_explored+=1

            for (action,state) in self.findChild(node.state):

                if not frontier.containsState(state) and state not in self.explored:

                    child=Node(state=state[0],cost=state[1],parent=node,action=action)
                    if state[0] == self.goal:
                        action = []
                        cells = []
                        while child.parent is not None:
                            action.append(child.action)
                            cells.append(child.state)
                            child=child.parent
                        action.reverse()
                        cells.reverse()
                        return (cells)
                    frontier.insert(child)

    def print_route(self):
        city=[]
        for elem in self.content:
            row=[]
            for word in elem:
                row.append(word)
            city+=row
        cordinates=solve(self)
        for (cordinate,cost) in cordinates:
            city[cordinate[0]][cordinate[1]]='+'
        for elem in city:
            elem=''.join(elem)
            print(elem)



map=Map('a.txt')
map.print_route()