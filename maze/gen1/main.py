from PIL import Image, ImageDraw, ImageTk
import random
import tkinter as tk
import customtkinter as ctk

class Rand_Depth_first_search:
    global mode
    mode = 'RGBA'

    def __init__(self, width=10, height=10) -> None:
        self.width = width
        self.height = height
        self.stack = []
        self.cell = []
        self.visited = []

        self._maze = Image.new(mode, (self.width+1, self.height+1), '#f000')
        self.generate_Default_Image()

        self.startPosition = self.__pickStartPosition()
        # print(self.startPosition)

        self.startAlgo()

        # print(self.stack)

    def startAlgo(self):
        # while (len(self.visited) != len(self.cell)):
        direction = ['north', 'east', 'south', 'west']
        
        current_cell = self.stack[len(self.stack)-1]
        neighbor = self.cell_neighbor(current_cell)

        side = direction[random.randint(0, 3)]
        goto = neighbor[side]


        if neighbor[direction[0]] == None and neighbor[direction[1]] == None and neighbor[direction[2]] == None and neighbor[direction[3]] == None:
            self.stack.pop()
            return
            # continue

        if goto == None:
            # continue
            return

        if side == 'north':
            ImageDraw.Draw(self._maze, mode).point((goto[0], goto[1]+1), '#0f0')
            ImageDraw.Draw(self._maze, mode).point(goto, '#0f0')
            self.stack.append(goto)
            self.visited.append(goto)
        elif side == 'east':
            ImageDraw.Draw(self._maze, mode).point((goto[0]-1, goto[1]), '#0f0')
            ImageDraw.Draw(self._maze, mode).point(goto, '#0f0')
            self.stack.append(goto)
            self.visited.append(goto)
        elif side == 'south':
            ImageDraw.Draw(self._maze, mode).point((goto[0], goto[1]-1), '#0f0')
            ImageDraw.Draw(self._maze, mode).point(goto, '#0f0')
            self.stack.append(goto)
            self.visited.append(goto)
        elif side == 'west':
            ImageDraw.Draw(self._maze, mode).point((goto[0]+1, goto[1]), '#0f0')
            ImageDraw.Draw(self._maze, mode).point(goto, '#0f0')
            self.stack.append(goto)
            self.visited.append(goto)

    def cell_neighbor(self, position: tuple[int, int]) -> dict:
        neighbor = {
            'north' : None,
            'east' : None,
            'south' : None,
            'west' : None
        }

        for n in neighbor:
            for i, j in self.cell:
                if n == 'north' and j + 2 == position[1]:
                    neighbor[n] = (position[0], j)
                    break
                if n == 'east' and i - 2 == position[0]:
                    neighbor[n] = (i, position[1])
                    break
                if n == 'south' and j - 2 == position[1]:
                    neighbor[n] = (position[0], j)
                    break
                if n == 'west' and i + 2 == position[0]:
                    neighbor[n] = (i, position[1])
                    break

        # check if the neighbor is visited and if so return to None
        for n in neighbor:
            if neighbor[n] in self.visited:
                neighbor[n] = None

        return neighbor

    def generate_Default_Image(self):
        color = ['black', 'white']
        for x in range(self.width+1):
            for y in range(self.height+1):
                if x in [0, self.width] or y in [0, self.height]:
                    ImageDraw.Draw(self._maze, mode).point((x, y), 'red')
                else:
                    if x%2 or y%2:
                        ImageDraw.Draw(self._maze, mode).point((x, y), color[(x+y)%2])
                        if color[(x+y)%2] == 'black':
                            self.cell.append((x,y))
                    else:
                        ImageDraw.Draw(self._maze, mode).point((x, y), 'white')

    def __pickStartPosition(self) -> dict:
        side = ['left', 'top', 'right', 'bottom']
        side = side[random.randrange(0, 4)]
        step = 2

        if side == 'left':
            position = (0, random.randrange(1, self.height, step))
        elif side == 'top':
            position = (random.randrange(1, self.width, step), 0)
        elif side == 'right':
            position = (self.width, random.randrange(1, self.height, step))
        elif side == 'bottom':
            position = (random.randrange(1, self.width, step), self.height)

        ImageDraw.Draw(self._maze, mode).point(position, '#0f0')
        ImageDraw.Draw(self._maze, mode).point((position[0] + (1 if side == 'left' else -1 if side == 'right' else 0), 
                                                position[1] + (1 if side == 'top' else -1 if side == 'bottom' else 0)), '#0f0')
        # self.__addStack(position)
        self.stack.append((position[0] + (1 if side == 'left' else -1 if side == 'right' else 0), 
                         position[1] + (1 if side == 'top' else -1 if side == 'bottom' else 0)))
        self.visited.append((position[0] + (1 if side == 'left' else -1 if side == 'right' else 0), 
                         position[1] + (1 if side == 'top' else -1 if side == 'bottom' else 0)))
        
        return {side: position}


def generateNew():
    global img, display, maze, width, height

    if 'display' in globals():
        display.destroy()

    width = xVar.get()
    height = yVar.get()
    maze = Rand_Depth_first_search(width, height)

    if width >= height:
        width, height = 350, int(350 * (height/width))
    else:
        width, height = int(350 * (width/height)), 350

    img = ImageTk.PhotoImage(maze._maze.resize((width, height), Image.NEAREST))
    
    display = tk.Label(frame, image=img)
    display.pack(expand=True, fill='both')

def nextPath():
    global img, display, maze

    if 'display' in globals():
        display.destroy()

    maze.startAlgo()
    img = ImageTk.PhotoImage(maze._maze.resize((width, height), Image.NEAREST))
    
    display = tk.Label(frame, image=img)
    display.pack(expand=True, fill='both')
    if len(maze.visited) != len(maze.cell):
        # print('--[ Running ]--')
        window.after(1, nextPath)
    else:
        print('--[ STOP ]--')

window = tk.Tk()
window.geometry('800x500+750+100')
window.resizable(False, False)
window.config(background='#252525')

frame = ctk.CTkFrame(window)
frame.pack(side='left', expand=True)
button = ctk.CTkFrame(frame)
button.pack()
form = ctk.CTkFrame(frame)
form.pack()

xVar = tk.IntVar()
yVar = tk.IntVar()
xVar.set(100)
yVar.set(100)
x = ctk.CTkEntry(form, placeholder_text='100', textvariable=xVar)
x.pack(side='left')
y = ctk.CTkEntry(form, placeholder_text='100', textvariable=yVar)
y.pack(side='left')

newBtn = ctk.CTkButton(button, text='New', command=generateNew)
newBtn.pack(pady=20, side='left')

generateBtn = ctk.CTkButton(button, text='Generate', command=nextPath)
generateBtn.pack(pady=20, side='left')

window.mainloop()
maze._maze.save('maze.png')