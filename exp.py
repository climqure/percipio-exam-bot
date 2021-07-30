from contextlib import nullcontext
from json import load
import pyautogui
import clipboard
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


# copy text from the active window
def copyText():
    sleep(0.2)
    pyautogui.moveTo(2200, 350)
    sleep(0.1)
    pyautogui.click()
    sleep(0.05)
    pyautogui.hotkey('ctrl', 'a')
    sleep(0.05)
    pyautogui.hotkey('ctrl', 'c')
    sleep(0.2)
    pyautogui.click(clicks=1)
    sleep(0.05)
    copiedText = clipboard.paste()
    return copiedText


# get number of questions for the session
def getNumber(text):
    questionNo = ''
    textArray = text.split('\n')
    if '1 of' in textArray[9] and questionNo == '':
        questionNo = textArray[9]
    if '1 of' in textArray[10] and questionNo == '':
        questionNo = textArray[10]
    if '1 of' in textArray[11] and questionNo == '':
        questionNo = textArray[11]

    print(questionNo)
    number = int(questionNo[-2:])
    print(number)
    return number

# parse text to select only the question and the answers and write to the text file
def parseText(text):
    textArray = text.split('\n')
    question = ''
    if ':' in textArray[11] and question == '':
        question = textArray[11]
    if ':' in textArray[12] and question == '':
        question = textArray[12]
    if ':' in textArray[13] and question == '':
        question = textArray[13]    
    answer = '\n'
    
    for i in range(len(textArray)):
        if textArray[i] == 'Correct answer.':
            answer += str(textArray[i-2]) + '\n'
    answer += '\n'

    # write the solution to the file on data.txt
    f = open('data.txt', 'a')
    f.write(question + answer)
    f.close()


loadSite = webdriver.Chrome(executable_path='/home/linux/Desktop/chromedriver', chrome_options= Options().add_experimental_option('detach', True))

# click submit answer in browser
def submitAns():
    try:
        act = loadSite.find_element_by_class_name('Button---primary---1O3lq')
        act.click()
    except ElementClickInterceptedException:
        pass
    sleep(0.3)


# click next question in browser
def nextQue():
    act = loadSite.find_element_by_class_name('Question---nextButton---CSHu3')
    act.click()
    sleep(0.1)


# click the radio button in browser
def radioButton():
    act = loadSite.find_element_by_class_name('RadioButton---label---1dtPw')
    act.click()
    sleep(0.1)


# click the checkbox button in browser
def checkBox():
    act = loadSite.find_element_by_class_name('Checkbox---checkboxContainer---2Hz1S')
    act.click()
    sleep(0.1)


# click Done button
def Done():
    act = loadSite.find_element_by_class_name('Question---finishButton---ANWvo')
    act.click()
    sleep(0.3)


# click the start new test button
def startNew():
    act = loadSite.find_element_by_class_name('Button---small---3PMLN')
    act.click()
    sleep(2)


# retrieve stored answer
def getAnswer(screenText):
    textArray = screenText.split('\n')
    question = ''
    if ':' in textArray[11] and question == '':
        question = textArray[11]
    if ':' in textArray[12] and question == '':
        question = textArray[12]
    if ':' in textArray[13] and question == '':
        question = textArray[13]   
    answer = []
    checker = 0

    file = open('data.txt', 'r')
    lines = file.readlines()

    for line in lines:
        if line != '\n' and checker == 1:
            answer.append(line.strip())

        if line == '\n' and checker == 1:
            break

        if line.strip() == question:
            checker = 1
    
    return answer



# select the right answer in the browser
def selectAnswer():
    answer = getAnswer(copyText())
    if answer == []:
        try:
            loadSite.find_element_by_class_name('RadioButton---label---1dtPw').click()
        except NoSuchElementException:
            loadSite.find_element_by_class_name('Checkbox---checkboxContainer---2Hz1S').click()

    if len(answer) == 1:
        try:
            loadSite.find_element_by_xpath("//*[text()='{}']".format(answer[0])).click()
        except NoSuchElementException:
            loadSite.find_element_by_class_name('RadioButton---label---1dtPw').click()
    else:
        for item in answer:
            try:
                loadSite.find_element_by_xpath("//*[text()='{}']".format(item)).click()
            except NoSuchElementException:
                loadSite.find_element_by_class_name('Checkbox---checkboxContainer---2Hz1S').click()


attempt = ''

while attempt == '':
    input("Load the website and enter any key to continue:...")

    # run the first cycle to get all the answers

    number = getNumber(copyText())

    for i in range(number):
        try:
            loadSite.find_element_by_class_name('RadioButton---label---1dtPw').click()
        except NoSuchElementException:
            loadSite.find_element_by_class_name('Checkbox---checkboxContainer---2Hz1S').click()
        submitAns()
        parseText(copyText())
        if i < number-1:
            sleep(1)
            nextQue()
        else:
            sleep(1)
            Done()


    # final attempt with all right answers
    sleep(4)
    startNew()

    for i in range(number):
        selectAnswer()
        submitAns()
        if i < number-1:
            sleep(1)
            nextQue()
        else:
            sleep(1)
            Done()
    
    # delete the content of the file data.txt
    f = open('data.txt', 'w')
    f.write('')
    f.close()

    print("All done")
    attempt = input("Press enter key to try another exam...")