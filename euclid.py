import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Euclid Contest Problem Generator")

import os
import glob
import requests
import secrets
import logging
import subprocess
from PIL import Image
from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise
from py_pdf_parser.components import PDFDocument
from py_pdf_parser.common import BoundingBox
from pdf2image import convert_from_path


logging.getLogger("PDFParser").setLevel(logging.ERROR)
logging.getLogger().disabled = True

subprocess.call("TASKKILL /F /IM Microsoft.Photos.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

range1 = []

print("Range of questions:")

while True:
    
    low = input("Lowest question number desired? ")

    if low.isnumeric() and int(low) <= 10 and int(low) >= 1:
        high = input("Highest question number desired? ")

        if high.isnumeric() and int(high) <= 10 and int(high) >= 1 and int(high) >= int(low):
            range1.append(int(low))
            range1.append(int(high))
            break

        else:
            print("Invalid input!")
    
    else:
        print("Invalid input!")


if not os.path.exists(os.getcwd() + '/files/'):
    os.makedirs(os.getcwd() + '/files/')

def get_sol(n, year):
    pnumber = 1

    crops = []

    url = "https://www.cemc.uwaterloo.ca/contests/past_contests/" + str(year) + "/" + str(year) + "EuclidSolution.pdf"
    response = requests.get(url)

    with open(os.getcwd() + "/files/" + str(year) + "sol.pdf", "wb") as f:
        f.write(response.content)

    doc = load_file(os.getcwd() + "/files/" + str(year) + "sol.pdf")
    #visualise(doc, page_number=2, show_info=True)

    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for x in doc.elements:
        for i in range(1, 11):
            if x.text()[0:2] == str(i) + "." and x.page_number != 1 and x.bounding_box.x0 < 85:
                if i in a:
                    arr = [x.page_number, x.bounding_box.x0, x.bounding_box.y1, x.bounding_box]
                    crops.append(arr)
                    a.remove(i)
            elif x.text()[0:3] == "10." and i == 10 and x.bounding_box.x0 < 100:
                arr = [x.page_number, x.bounding_box.x0, x.bounding_box.y1, x.bounding_box]
                crops.append(arr)

    pages = convert_from_path(os.getcwd() + "/files/" + str(year) + "sol.pdf", 500)

    for page in pages:
        page.save(os.getcwd() + '/files/' + str(year) + "_" + str(pnumber) + 'sol.jpg', 'JPEG')
        pnumber += 1

    def crop(x):
        if x != len(crops) - 1:
            length = crops[x+1][0] - crops[x][0] + 1

            for i in range(length):
                img = Image.open(os.getcwd() + '/files/' + str(year) + "_" + str(crops[x][0] + i) + "sol.jpg")

                if (i == 0):
                    y2 = img.height

                    area = (int((crops[x][1]/612) * img.width), int(((792 - crops[x][2])/792) * img.height) - 100, img.width, y2)
                    cropped_img = img.crop(area)
                    cropped_img.save(os.getcwd() + "/files/img.jpg")
                    cropped_img.show()

                elif (i != length - 1):
                    cropped_img = img
                    cropped_img.show()

                else:
                    y2 = int(((792 - crops[x+1][2])/792) * img.height)

                    #if int(((792 - crops[x][2])/792) * img.height) - 100 > int(((792 - crops[x+1][2])/792) * img.height):
                        #y2 = img.height

                    area = (int((crops[x][1]/612) * img.width), 0, img.width, y2)
                    cropped_img = img.crop(area)
                    cropped_img.save(os.getcwd() + "/files/img.jpg")

                    if y2 > 375:
                        cropped_img.show()
        else:
            length = pnumber - crops[x][0] + 1

            for i in range(length):
                img = Image.open(os.getcwd() + '/files/' + str(year) + "_" + str(crops[x][0] + i) + "sol.jpg")

                if (i == 0):
                    y2 = img.height

                    area = (int((crops[x][1]/612) * img.width), int(((792 - crops[x][2])/792) * img.height) - 100, img.width, y2)
                    cropped_img = img.crop(area)
                    cropped_img.save(os.getcwd() + "/files/img.jpg")
                    cropped_img.show()

                else:
                    cropped_img = img
                    cropped_img.show()

    crop(n)

    dir_to_delete = glob.glob(os.getcwd() + "/files/*")
    for f in dir_to_delete:
        os.remove(f)

def run():

    show_sol = False
    n = secrets.randbelow(range1[1] - range1[0] + 1) + range1[0] - 1
    year = secrets.randbelow(25) + 1998

    #n = 3
    #year = 2003
    pnumber = 1

    crops = []

    url = "https://www.cemc.uwaterloo.ca/contests/past_contests/" + str(year) + "/" + str(year) + "EuclidContest.pdf"
    response = requests.get(url)

    with open(os.getcwd() + "/files/" + str(year) + ".pdf", "wb") as f:
        f.write(response.content)

    doc = load_file(os.getcwd() + "/files/" + str(year) + ".pdf")

    for x in doc.elements:
        for i in range(1, 11):
            if x.text()[0:2] == str(i) + "." and x.page_number != 1:
                if (x.page_number == 2 and i < 5) or (x.page_number != 2):
                    if "read the instructions" not in x.text() and "For questions marked" not in x.text() and "answer booklet" not in x.text() and "expressed as exact numbers" not in x.text() and "except where otherwise" not in x.text():
                        arr = [x.page_number, x.bounding_box.x0, x.bounding_box.y1, x.bounding_box]
                        crops.append(arr)
            elif x.text()[0:3] == "10." and i == 10:
                arr = [x.page_number, x.bounding_box.x0, x.bounding_box.y1, x.bounding_box]
                crops.append(arr)
            elif "read the instructions" in x.text() or "For questions marked" in x.text() or "expressed as exact numbers" in x.text() or "except where otherwise" in x.text():
                for p in crops:
                    if p[0] >= x.page_number:
                        if p[2] <= x.bounding_box.y1:
                            pass
                        else:
                            crops.remove(p)
                    else:
                        crops.remove(p)

    pages = convert_from_path(os.getcwd() + "/files/" + str(year) + ".pdf", 500)

    for page in pages:
        page.save(os.getcwd() + '/files/' + str(year) + "_" + str(pnumber) + '.jpg', 'JPEG')
        pnumber += 1

    def crop(x):
        img = Image.open(os.getcwd() + '/files/' + str(year) + "_" + str(crops[x][0]) + ".jpg")

        if x != len(crops) - 1:
            y2 = int(((792 - crops[x+1][2])/792) * img.height)

            if int(((792 - crops[x][2])/792) * img.height) - 100 > int(((792 - crops[x+1][2])/792) * img.height):
                y2 = img.height

            area = (int((crops[x][1]/612) * img.width), int(((792 - crops[x][2])/792) * img.height) - 100, img.width, y2)
            cropped_img = img.crop(area)
            cropped_img.save(os.getcwd() + "/files/img.jpg")
            cropped_img.show()

        else:
            y2 = img.height
            area = (int((crops[x][1]/612) * img.width), int(((792 - crops[x][2])/792) * img.height) - 100, img.width, y2)
            cropped_img = img.crop(area)
            cropped_img.save(os.getcwd() + "/files/img.jpg")
            cropped_img.show()

    print("Year: " + str(year) + ", Question number: " + str(n + 1))

    crop(n)

    while True:
        sol = input("Would you like to see the solution [Y/n]? ")

        if sol.lower() == "y" or sol.lower() == "":
            show_sol = True
            break

        elif sol.lower() == "n":
            break

        else:
            print("Invalid input!")

    if show_sol == True:
        get_sol(n, year)

    dir_to_delete = glob.glob(os.getcwd() + "/files/*")
    for f in dir_to_delete:
        os.remove(f)

counter = 0

while True:
    new_q = False

    while True:

        if (counter == 0):
            counter += 1
            new_q = True
            break
        
        else:
            new = input("Would you like another question [Y/n]? ")

            if new.lower() == "y" or new.lower() == "":
                new_q = True
                break

            elif new.lower() == "n":
                break

            else:
                print("Invalid input!")

    if new_q:
        subprocess.call("TASKKILL /F /IM Microsoft.Photos.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run()
    else:
        break