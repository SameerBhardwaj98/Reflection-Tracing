from tkinter import *
from collections import deque

#Global variables
GridMax = (0,0)
GridMin = (0,0)
top = ((0,0),(0,0))
left = ((0,0),(0,0))
right = ((0,0),(0,0))
bottom = ((0,0),(0,0))
time = 300
x = (0,0)
st = (0,0)
reflections = ()
buttons = []
shooter = 0
target = 0

#It generates  mirror reflections(one in each direction) for a given point 'x'
def generate(x):
    y = ()
    if x[1] < GridMax[1]:
        y = y + ((x[0],GridMax[1] + (GridMax[1] - x[1])),)
    if x[1] > GridMin[1]:
        y = y + ((x[0],GridMin[1] - ( -GridMin[1] +x[1]) ),)
    if x[0] < GridMax[0]:
        y = y + ((GridMax[0] + (GridMax[0] - x[0]),x[1]),)
    if x[0] > GridMin[0]:
        y = y + ((GridMin[0]- (-GridMin[0] + x[0]),x[1]),)
    return list(y)

#Function to create a circle on the canvas
def create_circle(x, y, r, canvasName,clr): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill = clr)

#It checks if the point x lies on the line formed by the pair of points y
def satisfy(y,x):
    if (x[1] - y[0][1]) * (x[0] - y[1][0]) == (x[1] - y[1][1]) * (x[0] - y[0][0]):
        return True
    return False

#It finds the point of intersection between the lines formed by the pairs l1 and l2
def intersection(l1,l2):
    '''
    m1x - m1x1 + y1 = m2x - m2x2 + y2
    x = (y2 - m2x2 - y1 + m1x1)/(m1 - m2)
    y = m1x - mx1 + y1
    a.y - b.y/a.x - b.x == c.y - d.y/c.x - d.x
    (a.y - b.y)*(c.x - d.x) = (c.y - d.y)*(a.x - b.x)
    m1x - m1x1 + y1 = m2x - m2x2 + y2
    x = (y2 - m2x2 - y1 + m1x1)/(m1-m2)
     '''
    if (l1[0][1] - l1[1][1]) * (l2[0][0] - l2[1][0]) == (l2[0][1] - l2[1][1]) * (l1[0][0] - l1[1][0]):
        print(l1)
        print(l2)
        print("yes")
        return (-1,-1)
    if l1[0][0] - l1[1][0] == 0 or l2[0][0] - l2[1][0] == 0:
        if l1[0][0] - l1[1][0] == 0:
            x = l1[0][0]
            m2 = (l2[0][1] - l2[1][1]) / (l2[0][0] - l2[1][0])
            y = m2*x - m2*l2[1][0] + l2[1][1]
            return (x,y)
        else:
            x = l2[0][0]
            m1 = (l1[0][1] - l1[1][1]) / (l1[0][0] - l1[1][0])
            y = m1 * x - m1 * l1[1][0] + l1[1][1]
            return (x,y)
    m1 = (l1[0][1] - l1[1][1]) / (l1[0][0] - l1[1][0])
    m2 = (l2[0][1] - l2[1][1]) / (l2[0][0] - l2[1][0])
    x = (- m2*l2[1][0] + l2[1][1] + m1*l1[1][0] - l1[1][1]) / (m1-m2)
    y = m1*x - m1*l1[1][0] + l1[1][1]
    return (x,y)

#It checks if the point z lies on the perimeter of the grid
def valid(z,str):
    global GridMin
    global GridMax
    if str == 'top' or str == 'bottom':
        if z[0] >= GridMin[0] and z[0] <= GridMax[0]:
            return True
        else:
            return False
    if str == 'right' or str == 'left':
        if z[1] >= GridMin[1] and z[1] <= GridMax[1]:
            return True
        else:
            return False

#It checks if the point c lies between the line segment formed by points a and b
def sameSlope(a,b,c):
    x1,x2,x3 = a[0],b[0],c[0]
    y1,y2,y3 = a[1],b[1],c[1]
    if x1 == x2 and x2 == x3:
        return (x3==x2) and ( (y1<=y3<=y2) or (y1 >= y3 >= y2) )
    elif x1 == x2 or x2 == x3 or x1 == x2:
        return False
    m = (y2 - y1) / (x2 - x1)
    pt3_on = (y3 - y1) * (x2 - x1) - (y2 - y1) * (x3 - x1) <= 0.1
    pt3_between = (min(x1,x2) < x3 < max(x1,x2)) and (min(y1,y2) < y3 < max(y1,y2))
    return pt3_on and pt3_between

#This function prints the whole trajectory of the beam
def createLine(st,tr,en,myCanvas,time = time):
    y = (st,tr)
    if satisfy(y,en):
        id = myCanvas.create_line(st[0],st[1],en[0],en[1],fill = 'green',arrow = LAST)
        myCanvas.after(time, myCanvas.delete, id)
        return
    z = intersection(top, y)
    if valid(z,'top') and sameSlope(tr,st,z):
        id = myCanvas.create_line(st[0], st[1], z[0], z[1],fill = 'green',arrow = LAST)
        myCanvas.after(time, myCanvas.delete, id)
        createLine(z,(tr[0],2*GridMin[1] - tr[1]),en,myCanvas,time)
        return
    z = intersection(right, y)
    if valid(z,'right') and sameSlope(tr,st,z):
        id = myCanvas.create_line(st[0], st[1], z[0], z[1],fill = 'green',arrow = LAST)
        myCanvas.after(time, myCanvas.delete, id)
        createLine(z, (2 * GridMax[0] - tr[0],tr[1]), en,myCanvas,time)
        return
    z = intersection(left, y)
    if valid(z,'left') and sameSlope(tr,st,z):
        id = myCanvas.create_line(st[0], st[1], z[0], z[1],fill = 'green',arrow = LAST)
        myCanvas.after(time, myCanvas.delete, id)
        createLine(z, (2*GridMin[0] - tr[0],tr[1]), en,myCanvas,time)
        return
    z = intersection(bottom, y)
    if valid(z,'bottom') and sameSlope(tr,st,z):
        id = myCanvas.create_line(st[0], st[1], z[0], z[1],fill = 'green',arrow = LAST)
        myCanvas.after(time,myCanvas.delete,id)
        #createLine(z, (tr[0], 2 * GridMin[1] - tr[1]), en, myCanvas)
        createLine(z, (tr[0],2*GridMax[1] - tr[1]), en,myCanvas,time)
        return

#This function displays the trajectories for aiming at all the targets one by one
def display(reflections,i,st,myCanvas,en):
    global time
    if i == len(reflections):
        return
    id = myCanvas.create_line(st[0],st[1],reflections[i][0],reflections[i][1],dash  = (3,2), fill = 'green',arrow = LAST)
    id2 = create_circle(reflections[i][0],reflections[i][1], 5, myCanvas, 'green')
    createLine(st,reflections[i],en,myCanvas)
    myCanvas.after(time,myCanvas.delete,id)
    myCanvas.after(time,myCanvas.delete,id2)
    myCanvas.after(time,display,reflections,i+1,st,myCanvas,en)

'''def reflectionPoint(e,st,en,myCanvas):
    global points
    print(points)
    id = myCanvas.create_line(st[0], st[1], points[int(e.get())][0], points[int(e.get())][1], dash=(5, 2), fill='green',arrow = LAST)
    createLine(st,points[int(e.get())],en,myCanvas,2000)
    myCanvas.after(2000, myCanvas.delete, id)
    print(e.get())'''

#This function is used for printing trajectory of the laser between shooter and a particular target(mirror image)
def reflectionPoint1(i,st,en,myCanvas):
    id = myCanvas.create_line(st[0], st[1], i[0], i[1], dash=(5, 2), fill='green',arrow = LAST)
    createLine(st,i,en,myCanvas,2500)
    myCanvas.after(2500, myCanvas.delete, id)
    #print(e.get())

#It sets the target inside the grid
def setTarget(e,myCanvas,b,b2):
    st = e.get().split(',')
    global target
    global x
    if len(st) == 2 and GridMin[0] < int(st[0]) + GridMin[0] < GridMax[0] and GridMin[1] < int(st[1]) + GridMin[1] < GridMax[1]:
        x = (int(st[0]) + GridMin[0],int(st[1]) + GridMin[1])
        target = create_circle(x[0], x[1], 5, myCanvas, 'red')
        b.configure(state = 'disabled')
        e.configure(state = 'disabled')
        b2.configure(state = 'normal')
#It sets the shooter inside the grid
def setShooter(e,myCanvas,b):
    global shooter
    st1 = e.get().split(',')
    global st
    if len(st1) == 2 and GridMin[0] < int(st1[0]) + GridMin[0] < GridMax[0] and GridMin[1] < int(st1[1]) + GridMin[1] < GridMax[1]:
        st = (int(st1[0]) + GridMin[0],int(st1[1]) + GridMin[1])
        shooter = create_circle(st[0], st[1], 5, myCanvas, 'green')
        b.configure(state='disabled')
        e.configure(state='disabled')

#It is used to generate all the mirror images of the target
def calculate2(x,myCanvas,b6):
    global reflections
    reflections = reflections + (x,)
    q = deque()
    m = {}
    c = 1
    m[x] = 1
    q.append(x)
    index = 0
    while q and c <= 16:
        z = q.popleft()
        y = generate(z)
        for i in y:
            if i not in m and c <= 16:
                m[i] = 1
                c += 1
                reflections = reflections + (i,)
                q.append(i)
                buttons.append(create_circle(i[0], i[1], 5, myCanvas, 'red'))
                myCanvas.tag_bind(buttons[index],"<Button-1>",lambda event, i=i : reflectionPoint1(i,st,x,myCanvas))
                index += 1
                # create_circle(i[0], i[1], 5, myCanvas,'red')
    b6.configure(state = 'disabled')
#It is used to reset all the widgets
def reset(myCanvas,b3,b4,e1,e2,b6):
    global buttons
    global reflections
    global shooter
    global target
    for i in buttons:
        myCanvas.delete(i)
    myCanvas.delete(shooter)
    myCanvas.delete(target)
    buttons = []
    reflections = ()
    b3.configure(state = 'normal')
    b4.configure(state = 'normal')
    e1.configure(state='normal')
    e2.configure(state='normal')
    e1.delete(0,'end')
    e2.delete(0,'end')
    b6.configure(state = 'disabled')


#This function is responsible for creating the window,the canvas and the buttons
def calculate():
    #reflections = ()
    #x = (x[0] + 400,x[1] + 400)
    global reflections
    global GridMax
    GridMax = (500, 500)
    global GridMin
    GridMin = (350,350)
    global top
    top = ((GridMin[0],GridMin[1]),(GridMax[0],GridMin[1]))
    global right
    right = ((GridMax[0],GridMin[1]),(GridMax[0],GridMax[1]))
    global left
    left = ((GridMin[0],GridMin[1]),(GridMin[0],GridMax[1]))
    global bottom
    bottom = ((GridMin[0],GridMax[1]),(GridMax[0],GridMax[1]))
    myWindow = Tk()
    myWindow.title("Reflection Tracing")
    myWindow.geometry('1300x1000')
    myCanvas = Canvas(myWindow,width='1000',height='1000',background = 'white')
    myCanvas.create_line(GridMin[0],GridMin[1],GridMax[0],GridMin[1],fill = 'black')
    myCanvas.create_line(GridMin[0],GridMin[1],GridMin[0],GridMax[1],fill = 'black')
    myCanvas.create_line(GridMin[0],GridMax[1], GridMax[1], GridMax[1],fill = 'black')
    myCanvas.create_line(GridMax[0], GridMin[1], GridMax[1], GridMax[1],fill = 'black')
    myCanvas.grid(row=0, column=0)
   # create_circle(x[0],x[1],5,myCanvas,'red')
    #myCanvas.pack()
    l1 = Label(myWindow, text='Enter the shooter position')
    l1.place(x=1000, y=90)
    e1 = Entry(myWindow)
    e1.place(x=1000, y=120)
    b3 = Button(myWindow, text = 'Set Shooter',command=lambda: setShooter(e1, myCanvas,b3))
    b3.place(x=1000, y= 150)
    l2 = Label(myWindow, text='Enter the target position')
    l2.place(x=1000, y=190)
    e2 = Entry(myWindow)
    e2.place(x=1000, y=220)
    b6 = Button(myWindow, text='Generate Reflections', command=lambda: calculate2(x, myCanvas,b6))
    b6.place(x=1000, y=300)
    b6.configure(state = 'disabled')
    b4 = Button(myWindow,text = 'Set Target', command=lambda: setTarget(e2, myCanvas,b4,b6))
    b4.place(x=1000, y=250)
    b = Button(myWindow,width = '10',height='1',text = 'Trace Paths',command = lambda : display(reflections,0,st,myCanvas,x))
    b.place(x = 1000,y = 340)
    b8 = Button(myWindow, width='10', height='1', text='Reset',command = lambda : reset(myCanvas,b3,b4,e1,e2,b6))
    b8.place(x=1000, y=380)
    myWindow.mainloop()

calculate()