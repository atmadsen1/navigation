import time
import myAlgorithm as alg
import nodeSmooth as ns
from tkinter import *

class simulation:
    #spacing and things are in pixels.
    def __init__ (self, width=500, height=500, spacing=50):
        self.width            = width
        self.height           = height
        self.spacing          = spacing
        self.objObstacle      = []
        self.objPath          = []
        self.obstacleMap      = []
        self.navigationPoints = [(0,0),(0,1)]   #start/end

    def openSimulation(self):
        self.root = Tk()
        self.optionFrame = Frame(self.root)

        self.C = Canvas(self.root, bg="tan", width=self.width, height=self.height)
        self.canvas_gridSetup()  #Used in canvas_removeObject() to not delete grid lines
        self.C.bind("<Button-1>",self.canvas_leftClick)
        self.C.bind("<Button-3>",self.canvas_rightClick)

        self.var = IntVar()
        self.R1 = Radiobutton(self.optionFrame, text="Obstacle",  variable=self.var, value=1, command=self.option_sel)
        self.R2 = Radiobutton(self.optionFrame, text="Start/End", variable=self.var, value=2, command=self.option_sel)
        self.R1.grid(row=0, column=0, sticky=W)
        self.R2.grid(row=1, column=0, sticky=W)
        self.startButton = Button(self.optionFrame, text="Path")
        self.startButton.bind("<Button-1>", self.findPath)
        self.startButton.grid(row=2, column=0, sticky=N)
        self.resObstButton = Button(self.optionFrame, text="Reset Obstacles")
        self.resObstButton.bind("<Button-1>", self.resetObstacles)
        self.resObstButton.grid(row=3, column=0, sticky=N)
        self.resPathButton = Button(self.optionFrame, text="Reset Path")
        self.resPathButton.bind("<Button-1>", self.resetPathing)
        self.resPathButton.grid(row=4, column=0, sticky=N)

        self.C.grid(row=0, column=0, sticky=W)
        self.optionFrame.grid(row=0, column=1, sticky=W)

        self.root.mainloop()

    def canvas_gridSetup(self):
        r = int(self.height/self.spacing)
        c = int(self.width/self.spacing)
        for row in range(1,r):  #Create horizontal grid lines
            coord = 0, (row*self.spacing), self.width, (row*self.spacing)
            self.C.create_line(coord, fill="gray", tag="grid")
        for col in range(1,c):  #Create vertical grid lines
            coord = (col*self.spacing), 0, (col*self.spacing), self.height
            self.C.create_line(coord, fill="gray", tag="grid")
        #Create start point
        xNorm = int(self.navigationPoints[0][1])
        yNorm = int(self.navigationPoints[0][0])
        coord = (xNorm*self.spacing), (yNorm*self.spacing), ((xNorm+1)*self.spacing), ((yNorm+1)*self.spacing)
        self.objStart = self.C.create_oval(coord, fill="blue")
        #Create end point
        xNorm = int(self.navigationPoints[1][1])
        yNorm = int(self.navigationPoints[1][0])
        coord = (xNorm*self.spacing), (yNorm*self.spacing), ((xNorm+1)*self.spacing), ((yNorm+1)*self.spacing)
        self.objEnd = self.C.create_oval(coord, fill="green")

    def canvas_leftClick(self,event):
        x, y = event.x, event.y
        xNorm = int(x/self.spacing)
        yNorm = int(y/self.spacing)
        if (self.var.get() == 1):   #if trying to place obstacle
            #if something is already there
            if (self.obstacleMap.count((yNorm,xNorm)) or self.navigationPoints[0]==[yNorm,xNorm] or self.navigationPoints[1]==[yNorm,xNorm]):
                return
            self.obstacleMap.append((yNorm,xNorm))
            coord = (xNorm*self.spacing), (yNorm*self.spacing), ((xNorm+1)*self.spacing), ((yNorm+1)*self.spacing)
            self.objObstacle.append(self.C.create_oval(coord, fill="black"))
        elif (self.var.get() == 2): #if trying to place start point
            #if something is already there
            if (self.obstacleMap.count((yNorm,xNorm)) or self.navigationPoints[0]==[yNorm,xNorm] or self.navigationPoints[1]==[yNorm,xNorm]):
                return
            #delete old start point and add new
            row = self.navigationPoints[0][0]*self.spacing+(self.spacing/2)
            col = self.navigationPoints[0][1]*self.spacing+(self.spacing/2)
            self.C.delete(self.objStart)
            self.navigationPoints[0] = [yNorm,xNorm]
            coord = (xNorm*self.spacing), (yNorm*self.spacing), ((xNorm+1)*self.spacing), ((yNorm+1)*self.spacing)
            self.objStart = self.C.create_oval(coord, fill="blue")
        self.resetPathing(event=event)

    def canvas_rightClick(self,event):
        x, y = event.x, event.y
        xNorm = int(x/self.spacing)
        yNorm = int(y/self.spacing)
        if (self.var.get() == 1):
            if (self.obstacleMap.count((yNorm,xNorm))):
                target = self.C.find_closest(x, y, start="grid")
                if (self.objObstacle.count(target[0])):   #make sure the target is an obstacle
                    self.C.delete(target)
                self.obstacleMap.remove((yNorm,xNorm))
            else:
                return
        elif (self.var.get() == 2):
            if (self.obstacleMap.count((yNorm,xNorm)) or self.navigationPoints[0]==[yNorm,xNorm] or self.navigationPoints[1]==[yNorm,xNorm]):
                return
            #delete old end point and add new
            row = self.navigationPoints[1][0]*self.spacing+(self.spacing/2)
            col = self.navigationPoints[1][1]*self.spacing+(self.spacing/2)
            self.C.delete(self.objEnd)
            self.navigationPoints[1] = [yNorm,xNorm]
            coord = (xNorm*self.spacing), (yNorm*self.spacing), ((xNorm+1)*self.spacing), ((yNorm+1)*self.spacing)
            self.objEnd = self.C.create_oval(coord, fill="green")
        self.resetPathing(event=event)

    def option_sel(self):
       selection = self.var.get()
       print(selection)

    def resetPathing(self,event):
        for path in self.objPath:
            self.C.delete(path)

    def resetObstacles(self,event):
        for obst in self.objObstacle:
            self.C.delete(obst)
        self.obstacleMap.clear()
        self.resetPathing(event=event);

    def findPath(self,event):
        w = int(self.width/self.spacing)
        h = int(self.height/self.spacing)
        graph = alg.AStarGraph(obstacles=self.obstacleMap,width=w,height=h)
        result, cost = alg.AStarSearch(self.navigationPoints,(0,0), graph)
        betResult = ns.smoothPath(rawPath=result)
        print ("route", result)
        print ("cost", cost)
        for i in range(len(result)-1):  #draw algorithm path
            coord = (result[i][1]*self.spacing+self.spacing/2, result[i][0]*self.spacing+self.spacing/2,
                    result[i+1][1]*self.spacing+self.spacing/2, result[i+1][0]*self.spacing+self.spacing/2)
            self.objPath.append(self.C.create_line(coord, fill="red"))
        for i in range(len(betResult)-1):   #draw smoothed path
            coord = (betResult[i][1]*self.spacing+self.spacing/2, betResult[i][0]*self.spacing+self.spacing/2,
                    betResult[i+1][1]*self.spacing+self.spacing/2, betResult[i+1][0]*self.spacing+self.spacing/2)
            self.objPath.append(self.C.create_line(coord, fill="green"))



if __name__=="__main__":
    sim = simulation(spacing=20)
    sim.openSimulation()