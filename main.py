import kivy
kivy.require('1.7.2')
 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle
from random import *
from kivy.config import Config
Config.set('graphics','resizable',0) #don't make the app re-sizeable
#Graphics fix
 #this fixes drawing issues on some phones
Window.clearcolor = (0,0,0,1.)


MINPROB = 300
WALL_BLANK = 150

class WidgetDrawer(Widget):
    #This widget is used to draw all of the objects on the screen
    #it handles the following:
    # widget movement, size, positioning
    #whever a WidgetDrawer object is created, an image string needs to be specified
    #example:    wid - WidgetDrawer('./image.png')
 
    #objects of this class must be initiated with an image string
    #;You can use **kwargs to let your functions take an arbitrary number of keyword arguments
    #kwargs ; keyword arguments
    def __init__(self, imageStr, width, height, **kwargs): 
        super(WidgetDrawer, self).__init__(**kwargs) #this is part of the **kwargs notation
        #if you haven't seen with before, here's a link http://effbot.org/zone/python-with-statement.html     
        with self.canvas: 
            #setup a default size for the object
            #self.size = (Window.width*.002*25,Window.width*.002*25) 
            #self.size = (width*.002*25,height*.002*25) 
            self.size = (width ,height) 
            #self.size = (100, 100) 
            #this line creates a rectangle with the image drawn on top
            self.rect_bg=Rectangle(source=imageStr,pos=self.pos,size = self.size) 
            #this line calls the update_graphics_pos function every time the position variable is modified
            self.bind(pos=self.update_graphics_pos) 
            self.x = self.center_x
            self.y = self.center_y
            #center the widget 
            self.pos = (self.x,self.y) 
            #center the rectangle on the widget
            self.rect_bg.pos = self.pos 
 
    def update_graphics_pos(self, instance, value):
        #if the widgets position moves, the rectangle that contains the image is also moved
        self.rect_bg.pos = value  
    #use this function to change widget size        
    def setSize(self,width, height):
        with self.canvas:
            self.size = (width, height)
    
    #use this function to change widget position    
    def setPos(xpos,ypos):
        self.x = xpos
        self.y = ypos

class Wall(WidgetDrawer):
    
    velocity_x = NumericProperty(0) #initialize velocity_x and velocity_y
    velocity_y = NumericProperty(0) #declaring variables is not necessary in python
    #update the position using the velocity defined here. every time move is called we change the position by velocity_x  

    

    def move(self):                    
        self.x = self.x + self.velocity_x 
        self.y = self.y + self.velocity_y 
    def update(self): 
#the update function moves the astreoid. Other things could happen here as well (speed changes for example)       
        self.move()

class Bird(WidgetDrawer):
    #Bird class. This is for the main bird object. 
    #velocity of ship on x/y axis
 
    impulse = 3 #this variable will be used to move the ship up
    grav = -0.1 #this variable will be used to pull the ship down
 
    velocity_x = NumericProperty(0) #we wont actually use x movement
    velocity_y = NumericProperty(0) 
 
    def move(self):                    
        self.x = self.x + self.velocity_x 
        self.y = self.y + self.velocity_y 
                
        #don't let the bird go too far
        if self.y > Window.height*0.95: #don't let the bird go up too high
            self.impulse = -3
        if self.y < Window.height*0.05: 
            self.impulse = 3
 
    def determineVelocity(self):
        #move the bird up and down
        #we need to take into account our acceleration
        #also want to look at gravity
        self.grav = self.grav*1.05  #the gravitational velocity should increase
        #set a grav limit
        if self.grav < -4: #set a maximum falling down speed (terminal velocity)
            self.grav = -4
        #the ship has a propety called self.impulse which is updated
        #whenever the player touches, pushing the bird up
        #use this impulse to determine the bird velocity
        #also decrease the magnitude of the impulse each time its used
 
        self.velocity_y = self.impulse + self.grav
        self.impulse = 0.95*self.impulse #make the upward velocity decay
 
    def update(self):
        self.determineVelocity() #first figure out the new velocity
        self.move()              #now move the ship

class MyButton(Button):
    #class used to get uniform button styles
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
 #all we're doing is setting the font size. more can be done later
        self.font_size = Window.width*0.018        

class GUI(Widget):
    #this is the main widget that contains the game. 
    wallList =[] #use this to keep track of walss
    minProb = 5 #this variable used in spawning walls
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        l = Label(text='Flappy Bird') #give the game a title
        l.x = Window.width/2 - l.width/2
        l.y = Window.height*0.8
        self.add_widget(l) #add the label to the screen
 
        #now we create a bird object
        #notice how we specify the bird image
        self.bird = Bird(imageStr = './bird.png', width=30, height=30)
        self.bird.x = Window.width/4
        self.bird.y = Window.height/2
        self.add_widget(self.bird)
 
    def addWall(self):
        #add an wall to the screen 
        
        #imageNumber = randint(1,4)
        #imageStr = './sandstone_'+str(imageNumber)+'.png'     
        imageStr = './wall_upper.png'

 
        #randomize y position
        ypos = randint(5,16)
 
        ypos = ypos*Window.height*.0625
        #ypos = 150

        tmpWall = Wall(imageStr, 50, Window.height - ypos)
        tmpWall.x = Window.width*0.99
 
        tmpWall.y = ypos
        tmpWall.velocity_y = 0
        vel = 10
        tmpWall.velocity_x = -0.1*vel
        #tmpWall.setSize(Window.width*.002*25, ypos* Window.width*.002*25)
        #tmpWall.setSize(1500, 1500)

        self.wallList.append(tmpWall)
        self.add_widget(tmpWall)
        
        imageStr_bottom = './wall_bottom.png'
        ypos = ypos - WALL_BLANK
        if ypos < 0:
            ypos = 0

        

        tmpWall = Wall(imageStr_bottom, 50, ypos)
        tmpWall.x = Window.width*0.99        
        
        tmpWall.y = 0
        tmpWall.velocity_y = 0
        vel = 10
        tmpWall.velocity_x = -0.1*vel

        self.wallList.append(tmpWall)
        self.add_widget(tmpWall)
        
    #handle input events
    #kivy has a great event handler. the on_touch_down function is already recognized 
    #and doesn't need t obe setup. Every time the screen is touched, the on_touch_down function is called
    def on_touch_down(self, touch):
        self.bird.impulse = 3 #give the ship an impulse
        self.bird.grav = -0.1 #reset the gravitational velocity
 
    def gameOver(self): #this function is called when the game ends
        #add a restart button
        restartButton = MyButton(text='Restart')
 
        #restartButton.background_color = (.5,.5,1,.2)
        def restart_button(obj):
        #this function will be called whenever the reset button is pushed
            print ('restart button pushed')
            #reset game
            for k in self.wallList:
                self.remove_widget(k)
 
                self.bird.xpos = Window.width*0.25
                self.bird.ypos = Window.height*0.5
                self.minProb = MINPROB
            self.wallList = []
 
            self.parent.remove_widget(restartButton)
 #stop the game clock in case it hasn't already been stopped
            Clock.unschedule(self.update)
 #start the game clock           
            Clock.schedule_interval(self.update, 1.0/60.0) 
        restartButton.size = (Window.width*.3,Window.width*.1)
        restartButton.pos = Window.width*0.5-restartButton.width/2, Window.height*0.5
        #bind the button using the built-in on_release event
        #whenever the button is released, the restart_button function is called       
        restartButton.bind(on_release=restart_button) 
 
        #*** It's important that the parent get the button so you can click on it
        #otherwise you can't click through the main game's canvas
        self.parent.add_widget(restartButton)
 
    def update(self,dt):
                #This update function is the main update function for the game
                #All of the game logic has its origin here 
                #events are setup here as well
        #update game objects
        #update bird
        self.bird.update()
        #update wall
        #randomly add an wall
        '''
        tmpCount = randint(1,1800)

        if tmpCount > self.minProb:            
            self.addWall()
            if self.minProb < 1300:
                self.minProb = 1300
            self.minProb = self.minProb -1
        '''
        if self.minProb == 0:
            self.addWall()
            self.minProb = MINPROB
        else:
            self.minProb = self.minProb -1
 
        for k in self.wallList:
            #check for collision with ship
            if k.collide_widget(self.bird):
                print ('death')
                #game over routine
                self.gameOver()
                Clock.unschedule(self.update)
                #add reset button
            k.update()

class ClientApp(App):
 
    def build(self):
        #this is where the root widget goes
        #should be a canvas
        parent = Widget() #this is an empty holder for buttons, etc
 
        app = GUI()        
        #Start the game clock (runs update function once every (1/60) seconds
        Clock.schedule_interval(app.update, 1.0/60.0) 
        parent.add_widget(app) #use this hierarchy to make it easy to deal w/buttons
        #print ("Window.width {:2d}".format(Window.width))
        return parent


if __name__ == '__main__' :
    ClientApp().run()
