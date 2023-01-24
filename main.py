from motor_code import *

class BOT:
    def __init__(self):
        self.orientation = 0 # 0 is North, 1 is East, 2 is South, 3 is West
        self.x=0
        self.y=0
        self.vis=set()
        self.to_explore=[]
        self.adj={}

    # Function to create information.
    def look_around(self,x,y,orientation):
        self.adj[(x,y)]=[]
        x_changer=[0,1,0,-1]
        y_changer=[1,0,-1,0]
        wall_checker=[is_wall_front(),is_wall_right(),is_wall_right(),is_wall_left()]
        for i in range(len(wall_checker)):
            if(wall_checker[i]==False):
                x_new = x + x_changer[(orientation+i)%4]
                y_new = y + y_changer[(orientation+i)%4]
                self.adj[(x, y)].append((x_new, y_new))
                if((x_new,y_new) not in self.vis):
                    self.to_explore.append((x + x_changer[(orientation+i)%4], y + y_changer[(orientation+i)%4]))

    # Next 4 functions commands the ways in which the bot moves
    def bot_turn_left(self,orientation):
        turn_left()
        return (orientation-1)%4

    def bot_turn_right(self,orientation):
        turn_right()
        return (orientation+1)%4

    def bot_move_forward(self,orientation):
        go_straight(1)
        return orientation

    def bot_move_backward(self,orientation):
        go_back(1)
        return orientation

    # Bot moves from x,y to x_new,y_new
    def move_adj(self,x,y,orientation,x_new,y_new):
        if(x_new-x==1):
            if(orientation==0):
                orientation=self.bot_move_forward(orientation)
            elif(orientation==1):
                orientation=self.bot_turn_left(orientation)
                orientation=self.bot_move_forward(orientation)
            elif(orientation==2):
                orientation=self.bot_move_backward(orientation)
            elif(orientation==3):
                orientation=self.bot_turn_right(orientation)
                orientation=self.bot_move_forward(orientation)
        elif(y_new-y==1):
            if(orientation == 0):
                orientation = self.bot_turn_right(orientation)
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 1):
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 2):
                orientation = self.bot_turn_left(orientation)
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 3):
                orientation = self.bot_move_backward(orientation)

        elif(x_new-x==-1):
            if (orientation == 0):
                orientation = self.bot_move_backward(orientation)
            elif (orientation == 1):
                orientation = self.bot_turn_right(orientation)
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 2):
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 3):
                orientation = self.bot_turn_left(orientation)
                orientation = self.bot_move_forward(orientation)

        elif(y_new-y==-1):
            if (orientation == 0):
                orientation = self.bot_turn_left(orientation)
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 1):
                orientation = self.bot_move_backward(orientation)
            elif (orientation == 2):
                orientation = self.bot_turn_right(orientation)
                orientation = self.bot_move_forward(orientation)
            elif (orientation == 3):
                orientation = self.bot_move_forward(orientation)
        self.vis.add((x_new,y_new))
        return orientation

    def find_path(self,x,y,x_new,y_new):
        parent={}
        bfs=[(x,y)]
        found_path=False
        path=[]
        while(found_path==False):
            bfs_new_layer=[]
            for i in bfs:
                for j in self.adj[i]:
                    bfs_new_layer.append(j)
                    parent[j]=i
                    if(j==(x_new,y_new)):
                        found_path=True
                        break
            bfs=bfs_new_layer.copy()
        while((x_new,y_new)!=(x,y)):
            path.append((x_new,y_new))
            (x_new,y_new)=parent[(x_new,y_new)]

        return path

    def move_to(self,x,y,orientation,x_new,y_new):
        path=self.find_path(x,y,x_new,y_new)
        while(path!=[]):
            temp_x=path[-1][0]
            temp_y=path[-1][1]
            orientation = self.move_adj(x,y,orientation,temp_x,temp_y)
            (x,y)=(temp_x,temp_y)
            path.pop()
        return orientation

    def first_iter(self):
        orientation=self.orientation
        x=self.x
        y=self.y
        self.vis.add((x, y))
        self.look_around(x, y, orientation)
        while(self.to_explore!=[]):
            (x_new,y_new)=self.to_explore.pop()
            orientation=self.move_to(x,y,orientation,x_new,y_new)
            x,y=x_new,y_new
            self.look_around(x,y,orientation)

        self.move_to(x,y,orientation,0,0)
        self.orientation=orientation

    def start(self):
        self.first_iter()
        orientation=self.orientation
        self.move_to(0,0,orientation,8,8)


bot = BOT()
bot.start()


