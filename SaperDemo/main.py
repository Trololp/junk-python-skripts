from PIL import ImageGrab
from PIL import ImageChops
from PIL import Image
import pygetwindow
import pyautogui
from Minesweepr import minesweeper_util
from Minesweepr import minesweeper
import random
import keyboard

Cell_width = 16
max_rows = 16
max_columns = 17
total_mines = 99
num_loses = 0
num_wins = 0

numbers_palleted = Image.open('numbers.bmp')
numbers = numbers_palleted.convert('RGB')
numbers_list = []
for i in range(3, 13):
    number_region = (0, i*23-23, 13, i*23)
    numbers_list.append(numbers.crop(number_region))
numbers.close()

faces_palleted = Image.open('face.bmp')
faces = faces_palleted.convert('RGB')
faces_list = []
for i in range(1, 6):
    faces_region = (0, i*24-24, 24, i*24)
    faces_list.append(faces.crop(faces_region))
faces.close()

tiles_colors = {
    (192, 192, 192): '.',
    (255, 255, 255): 'x',
    (128, 128, 128): '8',
    (0, 0, 0): '7',
    (0, 128, 128): '6',
    (128, 0, 0): '5',
    (0, 0, 128): '4',
    (255, 0, 0): '3',
    (0, 128, 0): '2',
    (0, 0, 255): '1',
}


faces_definitons = {
    0:'Fine',
    1:'End',
    2:'End',
    3:'Fine',
    4:'Fine',
}

def check_img_equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None


def select_tile_by_color(im1,x, y):
    pixel = im1.getpixel((8+x*16, 8+y*16))
    #print(im1.getpixel((8, 1)), pixel)
    if pixel == (192, 192, 192):
        if im1.getpixel((8+x*16, 1+y*16)) == (255, 255, 255):
            return 'x'

        return '.'
    return tiles_colors.get(pixel)


def click(x,y):
    pyautogui.mouseDown(x, y, 'left',0.01)
    pyautogui.mouseUp(x, y, 'left',0.01)


def recognize_board(cells_x, cells_y):
    cells = ''
    x = cells_x
    y = cells_y
    cell1 = (x, y, x + 16*max_columns, y + 16*max_rows)
    cell_image = ImageGrab.grab(cell1)
    for i in range(0, max_rows):
        for j in range(0, max_columns):

            #for check_icon in [0, 15, 14, 1, 12, 11, 10, 9, 8, 7, 13]:
               # if check_img_equal(cell_image, icons_list[check_icon]):
            cells += select_tile_by_color(cell_image, j, i)
        cells += '\n'
    return cells

def recognize_face(x,y):
    face1 = (x, y, x + 24, y + 24)
    face_image = ImageGrab.grab(face1)
    if check_img_equal(face_image, faces_list[1]):
        return 2
    elif check_img_equal(face_image, faces_list[2]):
        return 1
    else:
        return 0

def recognize_bombs_num(x, y):
    bomb_count = 0
    number1 = (x, y, x + 13, y + 23)
    num_image = ImageGrab.grab(number1)
    for i in range(0,10):
        if check_img_equal(num_image, numbers_list[i]):
            bomb_count += 100*(9-i)
    number2 = (x+13, y, x + 26, y + 23)
    num_image = ImageGrab.grab(number2)
    for i in range(0, 10):
        if check_img_equal(num_image, numbers_list[i]):
            bomb_count += 10 * (9 - i)
    number3 = (x+26, y, x + 39, y + 23)
    num_image = ImageGrab.grab(number3)
    for i in range(0, 10):
        if check_img_equal(num_image, numbers_list[i]):
            bomb_count += (9 - i)
    return bomb_count


def get_coord(key):
    if key is None:
        print("NONE passed throw")
    if (max_rows > 10 or max_columns > 10):
        y = int(key[0:2])
        x = int(key[3:5])
        return x, y
    x = int(key[2:3])
    y = int(key[0:1])
    return x, y






programm_name = 'Minesweeper'
windows = pygetwindow.getWindowsWithTitle(programm_name)

if len(windows) > 1:
    print("Please close the window with name Minesweeper or stay only one program")
    exit(1)

programm_window = windows[0]
window_left = programm_window.left
window_top =  programm_window.top
window_bottom = programm_window.bottom
window_right = programm_window.right
window_middle = (window_right+window_left)/2

restart_button = (window_middle, window_top+78)
bomb_count_topleft = (window_left+20, window_top+61)

max_columns = int(((window_right - window_left)-26)/16)
max_rows = int(((window_bottom-window_top)-111)/16)

total_mines = recognize_bombs_num(bomb_count_topleft[0], bomb_count_topleft[1])

cells_topleft = (window_left+15, window_top+100)

face_topleft = ((window_left+((30+max_columns*16)/2 - 12)), window_top+61)


def restart():
    click(window_left + 88, window_top + 228)
    click(window_left + 208, window_top + 221)
    click(restart_button[0], restart_button[1])
    click(cells_topleft[0] + random.randint(0, max_columns-1) * 16, cells_topleft[1] + random.randint(0, max_rows-1) * 16)




print(max_columns, max_rows)
print(total_mines)

random.seed()
programm_window.activate()
restart()





while True:

    if(keyboard.is_pressed('ESC') or keyboard.is_pressed('q')):
        break


    face_result = recognize_face(face_topleft[0], face_topleft[1])

    if(face_result):
        if(face_result == 2):
            num_wins += 1
            print(f"YOU WIN {num_wins} times")
            restart()
        if(face_result == 1):
            num_loses += 1
            print(f'YOU LOSE {num_loses} times')
            restart()

    Cells = recognize_board(cells_topleft[0], cells_topleft[1])
    rules = minesweeper_util.read_board(Cells, total_mines)

    #try:
    solution = minesweeper.solve(rules[0], rules[1])
    #except Exception:
    #    print("oops", Exception)
    #    restart()
    #    num_loses += 1
    #    continue

    click_cells = []
    posibilities_list = []

    for coord_key in solution.keys():
        if coord_key is None:
            continue
        if type(coord_key) == 'NoneType':
            continue
        if coord_key is not None:
            posibilities_list.append(solution.get(coord_key))


    clicking_cells = []
    cells_nums = 0
    min_posibility = min(posibilities_list)
    max_posibility = max(posibilities_list)
    if(min_posibility == max_posibility):
        if(min_posibility != 0.0):
            for coord_key in solution.keys():
                if coord_key is None:
                    continue
                if type(coord_key) == 'NoneType':
                    continue
                if (solution.get(coord_key) == min_posibility):
                    clicking_cells.append(coord_key)
                    cells_nums += 1
                    continue

            random_cell = random.randint(0, cells_nums-1)

            click(cells_topleft[0] + get_coord(clicking_cells[random_cell])[0] * 16,
                  cells_topleft[1] + get_coord(clicking_cells[random_cell])[1] * 16)
            continue


    if min_posibility != 0.0:
        print(f"Minimal posibility is {min_posibility}")

    for coord_key in solution.keys():
        if coord_key is None:
            continue
        if type(coord_key) == 'NoneType':
            continue
        if(solution.get(coord_key) == min_posibility):
            click_cells.append(get_coord(coord_key))

    for clicking_cell in click_cells:
        click(cells_topleft[0] + clicking_cell[0] * 16 - 16, cells_topleft[1] + clicking_cell[1]*16 - 16)

#for i in range(0,max_columns+1):
#    for j in range(0,max_rows+1):
#        click(cells_topleft[0]+i*16,cells_topleft[1]+j*16)

print(programm_window.title + 'AutoBot by Trololp')
