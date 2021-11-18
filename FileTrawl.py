import pyautogui                                #PYAUTOGUI is the main imput-handling library
import pyperclip                                #PYPERCLIP allows for clipboard manipulation
import time                                     #Used to allow pausing
import re                                       #Regular Expressions; allows for easy space removal
pyautogui.PAUSE = 0.25

def nextTabSave():                              #Function to move to next tab keeping current tab open
    pyautogui.hotkey('ctrl', 'tab')             #Next tab command
    time.sleep(0.75)                            #Pause to let page render

def nextTabClear():                             #Function to move to next tab while closing current 
    pyautogui.hotkey('ctrl', 'w')               #Close tab command
    time.sleep(0.75)                            #Pause to let page render

def publishAll(pubAll):                         #Function to publish file and relationships; call with location of publish relationships button
    pyautogui.moveTo(pubAll)                    #Move mouse to location of publish button
    pyautogui.click()                           #Click publish all
    pyautogui.press(['enter', 'esc', 'enter'])  #Close out of relationships menu
    pyautogui.press('p')                        #Open publish menu
    time.sleep(0.75)                            #Let menu open
    pyautogui.press('enter')                    #publish

def cleanText(text):
    text = text.lower()                         #Makes text lowercase
    text = re.sub(' +', '-', text)              #Converts spaces into -
    if (text[-4:] == "jpeg"):
        text = re.sub('\.','-', text[:-5]) + text[-5:]
    else:
        text = re.sub('\.', '-', text[:-4]) + text[-4:]
    text = re.sub('\-+', '-', text)
    return text                                 #Returns the text, now cleaned up!

def mainSlide(recFile, folderCenter, submitButton):           #Main remove function
    pyautogui.press("m")                              #Open move menu
    time.sleep(0.75)                                  #Allow time to let move menu open
    pyautogui.moveTo(folderCenter)                    #Move to new folder icon
    pyautogui.click()                                 #Click new folder icon
    time.sleep(0.75)                                  #Wait for slow menu to open
    pyautogui.moveTo(recFile)                         #Move to the most recent file folder
    pyautogui.click()                                 #Clicks most recent file
    pyautogui.press('enter')                          #Submits the new folder as location
    pyautogui.moveTo(submitButton)                    #Moves to the move submit button
    pyautogui.click()                                 #Click submit button
    nextTabClear()                              #Close this file
    return 1                                    #Success, complete

def mainCheck(nexFile, linkText):
    pyautogui.moveTo(nexFile)                   #Hover over next file
    pyautogui.middleClick()                     #Open next file in new tab 
    pyautogui.press('r')                        #Open rename 
    time.sleep(0.5)                             #Debug pause
    pyautogui.hotkey('ctrl', 'a')               #Select all of file title
    pyautogui.hotkey('ctrl', 'c')               #Copy name into clipboard
    fileName = pyperclip.paste()                #fileName is the name of the file
    fileName = cleanText(fileName)              #Remove spaces and caps. Leaves _'s.
    pyperclip.copy(fileName)                    #Copies new filename into clipboard
    pyautogui.hotkey('ctrl', 'v')               #Pastes text back into field.
    if ((fileName[-4] != '.') and (fileName[-5:]!= ".jpeg")):                   #If the 4th to last character of fileName is not a .
        print("Error - unknown filetype.")      #Filetype not found; tell user.
        nextTabSave()                           #Move onto next tabe, leaving this tab behind to be reviewed.
        return 0                                #Don't check for relationships, just move on
    time.sleep(0.5)                             #Sleep to ensure Cascade does not throw an "Are you sure?" -> If enter is pressed too quickly Cascade gets mad.
    pyautogui.press('enter')                    #Confirm rename
    pyautogui.press('l')                        #Open relationships
    time.sleep(0.5)                             #Pause to pull up relationships menu
    pyautogui.moveTo(linkText)                  #Move to section where text will only appear with relationships
    pyautogui.doubleClick()                     #Highlight
    pyautogui.hotkey('ctrl', 'c')               #Copy
    if (pyperclip.paste() != 'Linked'):         #If no text selected
        print("Error: No relationships.")       #Let user know there are no relationships
        print(pyperclip.paste())                #Prints the file name, so I can be CERTAIN it is removed
        mainSlide(recFile, folderCenter, submitButton)                           #Move to next
        pyautogui.press('f5')                   #Refresh the page
        time.sleep(0.75)                        #Let the page scroll down because of how silly cascade is
        return 0                                #Error detected - return 0
    else:                                       #If triggered, there are relationships (good case)
        publishAll(pubAll)                      #Publish the file
        nextTabClear()                          #Go to the next file
        print("Success - file acceptable")      #Just a print so that I can easily tell when 
        return 1                                #Success - return 1
    
if __name__ == "__main__":
    correctCount = 0                             #Counter of files without errors
    count=0                                      #File counter
    #screenWidth, screenHeight = pyautogui.size() #Get screen size (Not used)
    #currFile = [109, 547]                        #CONFIGURE TO OWN COMPUTER
    nexFile = [109, 578]                        #CONFIGURE TO OWN COMPUTER
    pubAll = [513, 375]                         #CONFIGURE TO OWN COMPUTER
    linkText = [1131, 497]                      #CONFIGURE TO OWN COMPUTER
    recFile = [1150, 418]                       #Location of the move to area
    folderCenter = [542, 276]                   #Location of the folder you have to click on at the beginning of a move operation
    submitButton = [1214, 136]                  #Location of the submit button
    TTotal = time.time()                        #Variable for timing the total runtime (used because I like data)
    #mainCheck(nexFile, linkText)                 #DEBUG - individual call of main check
    #curX, curY = pyautogui.position()           #DEBUG - USE AS POSITION FINDER
    #print(curX, curY)                           #DEBUG - USE AS POSITION FINDER
    try:                                         #While exception not thrown
        while True:                              #While loop
            time.sleep(0.25)                     #Too many damn files
            t = time.time()                      #Variable for timing length of file audit (used for optimization)
            correctCount = correctCount + mainCheck(nexFile, linkText)             #Call main check
            count = count + 1                    #Upon finish, add 1 to count
            print("File time: " + str(time.time() - t))
    except:                                      #When exception is thrown, output
        print("Trawl complete. \n Successfully scanned ~" + str(count) + " documents.")       #OUTPUT
        print("Of these documents, " + str(correctCount) + " had no errors!")                   #OUTPUT
        print("Elapsed time: " + str(time.time() - TTotal))
