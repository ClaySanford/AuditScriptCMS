import pyautogui                                #PYAUTOGUI is the main imput-handling library
import pyperclip                                #PYPERCLIP allows for clipboard manipulation
import time                                     #Used to allow pausing
import re                                       #Regular Expressions; allows for easy space removal
pyautogui.PAUSE = 0.75

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
    time.sleep(0.75)                            #Pause to let tab render
    pyautogui.press(['enter', 'enter'])         #Double tap enter in case of "Are you sure?" prompt

def cleanText(text):
    text = text.lower()                         #Makes text lowercase
    text = re.sub(' +', '-', text)              #Converts spaces into -
    return text                                 #Returns the text, now cleaned up!

def mainCheck(nexFile, linkText):
    pyautogui.moveTo(nexFile)                   #Hover over next file
    pyautogui.middleClick()                     #Open next file in new tab 
    pyautogui.press('r')                        #Open rename 
    #time.sleep(0.5)                             #Debug pause
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
    pyautogui.press(['enter'])                  #Confirm rename
    pyautogui.press('l')                        #Open relationships
    pyautogui.moveTo(linkText)                  #Move to section where text will only appear with relationships
    pyautogui.doubleClick()                     #Highlight
    pyperclip.copy('.')                         #Clears the clipboard
    pyautogui.hotkey('ctrl', 'c')               #Copy
    if (pyperclip.paste() == '.'):              #If no text selected
        print("Error: No relationships.")       #Let user know there are no relationships
        nextTabSave()                           #Move to next
        return 0                                #Error detected - return 0
    else:                                       #If triggered, there are relationships (good case)
        publishAll(pubAll)                      #Publish the file
        nextTabClear()                          #Go to the next file
        return 1                                #Success - return 1
    
if __name__ == "__main__":
    correctCount = 0                             #Counter of files without errors
    count=0                                      #File counter
    #screenWidth, screenHeight = pyautogui.size() #Get screen size (Not used)
    #currFile = [109, 547]                        #CONFIGURE TO OWN COMPUTER
    nexFile = [109, 578]                         #CONFIGURE TO OWN COMPUTER
    pubAll = [513, 375]                          #CONFIGURE TO OWN COMPUTER
    link = [1131, 497]                           #CONFIGURE TO OWN COMPUTER
    #mainCheck(nexFile, pubAll)                 #DEBUG - individual call of main check
    #curX, curY = pyautogui.position()           #DEBUG - USE AS POSITION FINDER
    #print(curX, curY)                           #DEBUG - USE AS POSITION FINDER
    try:                                         #While exception not thrown
        while True:                              #While loop
            correctCount = correctCount + mainCheck(nexFile, link)             #Call main check
            count = count + 1                    #Upon finish, add 1 to count
    except:                                      #When exception is thrown, output
        print("Trawl complete. \n Successfully scanned ~" + str(count) + " documents.")       #OUTPUT
        print("Of these documents, " + str(correctCount) + " had no errors!")                   #OUTPUT
        
