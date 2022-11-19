import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def loadData(f1):
    endparse = True

    print("LOADING PAGES UNTIL LAST 5 IN PAGE ARE ALL LOWER THAN UPVOTE THRESHOLD")

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while (endparse == True):

        endparse = False

        likes = driver.find_elements(By.CLASS_NAME, "src-components-common-comment-__comment_---pcCommentWrap---DcvmRu")

        for item in likes[-5:]:
            for elem in item.find_elements(By.XPATH, ".//*"):
                if (elem.text.isnumeric() and int(elem.text) >= threshold):
                    endparse = True
                    break
            if (endparse):
                break

        print("PARSING NEXT PAGE")

        if (endparse == False):
            break

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    teamaggregates = driver.find_elements(By.CLASS_NAME, "src-components-pc-lineCard-__card_---lineCard---HYQyCO")

    validteams = []

    print("FILTERING TEAMS TO ONES ABOVE UPVOTE THRESHOLD")

    for item in teamaggregates:
        next = False
        for elem in item.find_elements(By.CLASS_NAME, "src-components-common-comment-__comment_---pcCommentWrap---DcvmRu"):
            elemvalues = elem.text.splitlines()
            for val in elemvalues:
                if (val.isnumeric() and int(val) >= threshold):
                    validteams.append(item.find_element(By.CLASS_NAME, "src-components-pc-lineCard-__card_---wholeGroup---PW3Zr3"))
                    next = True
                    break
            if next:
                break

    print("CONVERTING AND WRITING TO CSV")

    for item in validteams:
        team = item.find_elements(By.CLASS_NAME, "src-components-pc-avatar-__ava_---ava---svrjMB")
        counter = 0
        for character in team:
            attributeValue = character.get_attribute("style")
            if attributeValue == "":
                continue
            attributeValue = attributeValue.replace('background-image: url("', '')
            attributeValue = attributeValue.replace('");', '')
            characterName = playerlinks[attributeValue]
            if characterName == 'Traveler':
                element = character.find_elements(By.XPATH, ".//*")[0].find_elements(By.XPATH, ".//*")[0]
                if "wind" in element.get_attribute("class"):
                    characterName += 'Anemo'
                elif "frost" in element.get_attribute("class"):
                    characterName += 'Cryo'
                elif "grass" in element.get_attribute("class"):
                    characterName += 'Dendro'
                elif "elect" in element.get_attribute("class"):
                    characterName += 'Electro'
                elif "roach" in element.get_attribute("class"):
                    characterName += 'Geo'
                elif "water" in element.get_attribute("class"):
                    characterName += 'Hydro'
                elif "fire" in element.get_attribute("class"):
                    characterName += 'Pyro'
            f1.write(characterName)
            if counter < 3:
                f1.write(",")
            counter += 1
        f1.write("\n")

    print("COMPLETE")

# Main function start
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("PULLING DATA FROM MIHOYO LINEUP SIMULATOR")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

tabs = ["Applicable for Abyssal Moon Spire", "12-3", "12-2", "12-1"]
threshold = 25
SCROLL_PAUSE_TIME = 2.0

playerlinks = {}

driver = webdriver.Chrome()
driver.get("https://act.hoyolab.com/ys/event/bbs-lineup-ys-sea/index.html")

print("LOADING PAGE")

# sleep for some time
time.sleep(3)

print("SELECTING SPIRAL ABYSS")

driver.find_element("xpath", "//li[contains(text(),\
'Spiral Abyss')]").click()

time.sleep(1)

print("LOADING CHARACTER PROFILE IMAGE LINKS")

driver.find_element("xpath", "//p[contains(text(),\
'Filter Characters')]").click()

time.sleep(1)

characterfilter = driver.find_element(By.CLASS_NAME, "src-components-pc-filter-__filter_---role---yVYdvb").find_elements(By.CLASS_NAME, "src-components-pc-avatar-__ava_---ava---svrjMB")

characterNames = driver.find_element(By.CLASS_NAME, "src-components-pc-filter-__filter_---role---yVYdvb").find_elements(By.CLASS_NAME, "src-components-pc-avatar-__ava_---roleName---exjxM7")

for i in range(0, len(characterfilter)):
    imageLink = characterfilter[i].get_attribute("style")
    imageLink = imageLink.replace('background-image: url("', '')
    imageLink = imageLink.replace('");', '')
    playerlinks[imageLink] = characterNames[i].text

driver.find_element("xpath", "//p[contains(text(),\
'Filter Characters')]").click()

time.sleep(1)

iterator = 0

with open("./inputs/genshinTeamsExportFromMihoyo.csv",'w') as f1:
    for tab in tabs:
        print("FILTERING BY UPPER ABYSS FLOORS")

        if iterator == 0:
            driver.find_element("xpath", "//p[contains(text(),\
            'Applicable Scenarios')]").click()
        
        else:
            clickTab = "//p[contains(text(),\
            '{}')]".format(tabs[iterator - 1])

            driver.find_element("xpath", clickTab).click()

        time.sleep(1)

        driver.find_element("xpath", "//span[contains(text(),\
        'Abyssal Moon Spire')]").click()

        time.sleep(1)

        elemTab = "//span[contains(text(),\
        '{}')]".format(tab)

        driver.find_element("xpath", elemTab).click()

        time.sleep(3)

        loadData(f1)

        time.sleep(1)

        iterator += 1

f1.close()
driver.close()

print("COMPLETE")