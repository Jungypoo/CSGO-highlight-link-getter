import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

linkList = []
bigList = []
matchList = [
    'https://www.hltv.org/matches/2340841/fnatic-vs-vitality-esl-one-road-to-rio-europe',
    'https://www.hltv.org/matches/2340943/geng-vs-evil-geniuses-esl-one-road-to-rio-north-america',
    'https://www.hltv.org/matches/2340842/nip-vs-complexity-esl-one-road-to-rio-europe',
    'https://www.hltv.org/matches/2340943/geng-vs-evil-geniuses-esl-one-road-to-rio-north-america',
    'https://www.hltv.org/matches/2340868/mousesports-vs-g2-esl-one-road-to-rio-europe',
]

# For each URL in the Match List...
for i in range(len(matchList)):
    res = requests.get(matchList[i])
    soup = BeautifulSoup(res.text, 'html.parser')
    bob = soup.find_all(class_='highlight padding standard-box')

    # Grabbing each highlight link from the page
    for x in range(len(bob)):
        frank = bob[x].get('data-highlight-embed')

        # Getting rid of the embed and autoplay section of the URL
        cut1 = frank.find('embed')
        cut2 = frank.find('=') + 1
        frank = frank[:cut1] + frank[cut2:]
        frank = frank[:frank.find('&')]

        # Add it to the linkList
        linkList.append(frank)
        # if frank[-1] == "Z":
        # Weird thing I had to do because a Z was trailing at the end of a link
        #    del linkList[-1]
        #    print('Deleted the offending Z')
        print(frank)

print('\n*** ' + str(len(linkList)) + ' results collected ***\n')

# Do the Selenium thing
driver = webdriver.Firefox()
driver.get('https://clipr.xyz/')

# For each link in the Link List...
for i in range(len(linkList)):
    # Wait for the URL box at the start of the loop
    elem = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'clip_url'))
    )
    elem.clear()
    elem.send_keys(linkList[i])
    elem.send_keys(Keys.RETURN)

    # Wait for the Download button element to appear
    elem = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'CLICK TO DOWNLOAD'))
    )

    # Append the download link to linkList, then click Back
    bigList.append(elem.get_attribute('href'))
    driver.find_element_by_link_text('Back').click()

driver.close()

# Print out the results
for i in range(len(bigList)):
    print(bigList[i])
