###THIS SCRIPT DESIGNED TO MOVE UNUSED FILE TO >>>MOST RECENT<<< FILE FOLDER
import pyautogui as pyg
import time
import pyperclip
pyg.PAUSE = 0.75

def nextTabClear():                             #Function to move to next tab while closing current 
    pyg.hotkey('ctrl', 'w')               #Close tab command
    time.sleep(0.75)                            #Pause to let page render

def mainSlide(recFile, folderCenter, submitButton):           #Main remove function
    pyg.press("m")                              #Open move menu
    pyg.moveTo(folderCenter)                    #Move to new folder icon
    pyg.click()                                 #Click new folder icon
    pyg.moveTo(recFile)                         #Move to the most recent file folder
    pyg.click()                                 #Clicks most recent file
    pyg.press('enter')                          #Submits the new folder as location
    pyg.moveTo(submitButton)                    #Moves to the move submit button
    pyg.click()                                 #Click submit button
    nextTabClear()                              #Close this file
    return 1                                    #Success, complete

if __name__ == "__main__":
    recFile = [1150, 418]                       #Location of the move to area
    folderCenter = [542, 276]                   #Location of the folder you have to click on at the beginning of a move operation
    submitButton = [1214, 136]                  #Location of the submit button
    screenWidth, screenHeight = pyg.size()      #Get screen size (NOT USED)
    #curX, curY = pyg.position()                 #DEBUG - USE AS POSITION FINDER
    #print(curX, curY)                           #DEBUG - USE AS POSITION FINDER
    count = 0                                   #Counter
    pyg.moveTo(recFile)                         #Move mouse over window
    pyg.click()                                 #Click to focus on window
    #mainSlide(recFile, folderCenter, submitButton) #Debug call of a single main function
    try:                                        #Until exception is thrown
        while True:                             #Loop
            count = count + mainSlide(recFile, folderCenter, submitButton)#Call main and keep track
    except:                                     #After exception
        print("Movement complete.")             #Outputs finish
        print(" Successfully moved " + str(count) +" files!")#Outputs count
