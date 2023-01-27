import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def extractTeam(elements):
    result = []
    for element in elements:
        image = element.find_element(By.XPATH, ".//img").get_attribute("src")
        image = image[:-4]
        image = image[41:]
        # Convert mappings, if not mapping needed just Capitalize
        if image in mappings.keys():
            image = mappings[image]
        else:
            image = image.capitalize()
        result.append(image)
    return result

def loadData(f1):
    endparse = True
    pageNum = 1

    print("LOADING PAGES UNTIL TEAM DOES NOT HAVE AS MANY USES AS THRESHOLD")

    teamaggregates = []

    while (endparse == True):

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Pull team data
        divsbase = driver.find_element(By.ID, "team_list_table").find_element(By.TAG_NAME, 'tbody')
        teamdivs = []
        teamdivs += divsbase.find_elements(By.CLASS_NAME, "even")
        teamdivs += divsbase.find_elements(By.CLASS_NAME, "odd")

        # Parse each entry
        for item in teamdivs:
            # Grab completion counts, if less than threshold we stop
            teamCount = item.find_element("xpath", ".//td[contains(@class, 'dt-team-count')]").find_element("xpath", ".//div[contains(@class, 'fs-7 text-muted fw-bolder pt-1 text-center')]").text
            if int(teamCount) < threshold:
                endparse = False
                print("FOUND END OF LIST AT THRESHOLD CUTOFF, STOPPING")
                break

            # Pull data from first half
            right = item.find_element("xpath", ".//td[contains(@class, 'dt-right')]").find_element(By.XPATH, ".//div").find_elements("xpath", ".//div[contains(@class, 'team-image-div')]")
            teamaggregates.append(extractTeam(right))

            # Pull data from second half
            left = item.find_element("xpath", ".//td[contains(@class, 'dt-left')]").find_element(By.XPATH, ".//div").find_elements("xpath", ".//div[contains(@class, 'team-image-div')]")
            teamaggregates.append(extractTeam(left))

        # Next button
        pageNum += 1
        elementSearch = ".//li[contains(@class, 'paginate_button') and .//text()='" + str(pageNum) + "']"
        nextButton = driver.find_element("xpath", elementSearch).click()

        print("LOADING NEXT PAGE: " + str(pageNum))

    print("CONVERTING AND WRITING TO CSV")

    for team in teamaggregates:
        if len(team) < 4:
            continue
        counter = 0
        for character in team:
            f1.write(character)
            if counter < 3:
                f1.write(",")
            counter += 1
        f1.write("\n")

mappings = {
    "pingzang": "Heizou",
    "alhatham": "Alhaitham",
    "yaemiko": "Yae",
    "shougun": "Raiden",
    "yunjin": "Yun Jin",
    "feiyan": "Yan Fei",
    "hutao": "Hu Tao",
    "traveler_girl": "Traveler"
}

# Main function start
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print("PULLING DATA FROM AKASHA DATA")
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

threshold = 15
SCROLL_PAUSE_TIME = 2.0

playerlinks = {}

driver = webdriver.Chrome()
driver.get("https://akashadata.com/team/")

print("LOADING PAGE")

# sleep for some time
time.sleep(5)

with open("./inputs/genshinTeamsExportFromAkashaData.csv",'w') as f1:
        print("LOADING DATA")

        loadData(f1)

f1.close()
driver.close()

print("COMPLETE")