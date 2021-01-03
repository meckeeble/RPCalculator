import win32gui
import pytesseract
from numpy import array
from time import sleep
from PIL import ImageGrab, Image, ImageEnhance
import cv2

def changeContrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def RPPull(): 

    # Path of tesseract executable 
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract'

    print("starting... Do not move anything")
    sleep(0.5)
    # Get LoL's open window
    try:
        leagueWindow = win32gui.FindWindow(None, "League of Legends")
    except:
        print("Cannot find League of Legends window. Is it open?")

    # Bring LoL's window to front
    win32gui.SetForegroundWindow(leagueWindow)
    
    sleep(0.5)
    
    # Convert LoL's window to image for reading
    windowRef = win32gui.GetWindowRect(leagueWindow)
    windowImage = ImageGrab.grab(bbox = windowRef)

    #Sections of the screen pertaining to required numbers
    #TODO - Adjust scaling for different screen resolutions
    priceImage = ImageGrab.grab(bbox = (windowRef[0]+78,windowRef[1]+500,windowRef[0]+983, windowRef[1]+520))
    discountImage = ImageGrab.grab(bbox = (windowRef[0]+75,windowRef[1]+430,windowRef[0]+990, windowRef[1]+460))
    currentRpImage = ImageGrab.grab(bbox = (windowRef[0]+955,windowRef[1]+4,windowRef[0]+1040, windowRef[1]+60))


    # Adjust images for more accurate image reading...
    windowImage = changeContrast(windowImage,100)
    
    brightnessObj = ImageEnhance.Brightness(priceImage)
    priceImage = brightnessObj.enhance(0.5)
    
    brightnessObj = ImageEnhance.Brightness(discountImage)
    discountImage = brightnessObj.enhance(0.5)


    currentRpImage = currentRpImage.resize( ( (1040-955) *3, (60-4)*3 ), Image.ANTIALIAS)
    
    
    # Save reference images
    im = windowImage.save("ShopView.png")
    im2 = priceImage.save("prices.png")
    im3 = discountImage.save("discount.png")
    im3 = currentRpImage.save("RP.png")
    
    # OCR those bad boys 
    windowImageGet = pytesseract.image_to_string( windowImage, lang ='eng')
    priceImageGet = pytesseract.image_to_string(cv2.cvtColor(array(priceImage), cv2.COLOR_BGR2GRAY), lang ='eng')
    discountImageGet = pytesseract.image_to_string( discountImage, lang ='eng')
    currentRpImageGet = pytesseract.image_to_string( cv2.cvtColor(array(currentRpImage), cv2.COLOR_BGR2GRAY), lang ='eng')
    
    allImg = [windowImageGet,priceImage,discountImage,currentRpImage]
    
    print("Prices: ", [ i for i in priceImageGet.split() if i.isnumeric()])
    print("Discounts: ", [ i for i in discountImageGet.split() if "%" in i])
    print("Current RP: ", [ i for i in currentRpImageGet.split() if i.isdigit()][0]) #Detects RP symbol as "1)"

# Calling the function 
RPPull()

input("Enter key to exit")
