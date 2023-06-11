import requests
from bs4 import BeautifulSoup
import random
import string
import os
import time

#Asking user for a directory to download scraped images
downloadPath = str(input('Enter a directory to download scraped images.'))

#Headers to use
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

#Function to generate random URLS - Will make either a 5 or 6 letter long URL comprised of random letters and numbers
def ranStr3():
  baseUrl = 'https://prnt.sc/'
  randomExtension = (''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)))
  return(f'{baseUrl}{randomExtension}')

#Function to validate links - Done by checking the class of the image and also by seeing if it is the default "The screenshot was removed" image on the website
def validLink():
  baseUrl = ranStr3()
  query = requests.get(baseUrl, headers=headers)
  if query.status_code == 200:
    soup = BeautifulSoup(query.text, 'lxml')
    imageToScr = soup.findAll('img', class_ = 'no-click screenshot-image')
    for img in imageToScr:
      imgUrl = img.get('src')
      if 'st.prntscr.com/2023/05/26/0610/img/0_173a7b_211be8ff.png' in imgUrl:
        break
      else:
        return(baseUrl)

def main(downloadPath,maxImgs):
  count = 1
  #Further validation due to erroneous links that bypass the validLink function
  while count <= maxImgs:
    baseUrl = validLink()
    while baseUrl == False or baseUrl == None:
      baseUrl = validLink()
    query = requests.get(baseUrl, headers=headers)
    #Time.sleep in order to prevent getting IP banned :)
    time.sleep(1)
    if query.status_code == 200:
      soup = BeautifulSoup(query.text, 'lxml')
      imageToScr = soup.findAll('img', class_ = 'no-click screenshot-image', attempt = None)
      for img in imageToScr:
        imgUrl = img.get('src')
        imgResponse = requests.get(imgUrl, headers=headers)
        fName = imgUrl.split('/')[-1]
        with open(downloadPath + '\\' + fName, 'wb') as j:
          j.write(imgResponse.content)
        #Due to the nature of the website, some links still contain "images", except they are usually under a kilobyte in size and cannot be opened by Windows. This will read to the location of the downloaded png and will delete it if it is under the required size. 
        filePath = f'{downloadPath}{fName}'
        fileStats = os.stat(filePath)
        if fileStats.st_size < 1024:
          os.remove(filePath)
        else:
          print(f'fName: {fName}')
          count += 1

main(downloadPath,200)