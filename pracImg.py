from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

CDpath = "C:\Zone\code\Webscraping\chromedriver.exe"

wd = webdriver.Chrome(CDpath)

def getImages(wd, delay, maxImages):
  def scrollDown(wd):
    wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(delay)
  url = 'https://www.google.com/search?q=cats&rlz=1C1ONGR_enGB1051GB1051&sxsrf=APwXEdcD7W36RUDigKRop_O5W-VKqG-_zg:1685994516029&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjbjuKB86z_AhVYTUEAHdH3ApQQ_AUoAXoECAEQAw&biw=1280&bih=873&dpr=1'
  wd.get(url)
  
  imageUrls = set()
  skips = 0
  while len(imageUrls) + skips < maxImages:
    scrollDown(wd)
    thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')

    for img in thumbnails[len(imageUrls) + skips: maxImages]:
      try:
        img.click()
        time.sleep(delay)
      except:
        continue
      
      images = wd.find_elements(By.CLASS_NAME, 'r48jcc pT0Scc iPVvYb')
      for image in images:
        if image.get_attribute('src') in imageUrls:
          max_images += 1
          skips += 1
          break
        if image.get_attribute('src') and 'http' in image.get_attribute('src'):
          imageUrls.add(image.get_attribute('src'))
          print(f'Found {len(imageUrls)}')
  return imageUrls
  
def downloadImage(downloadPath, url, fileName):
  try:
    image_content = requests.get(url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    file_path = downloadPath + fileName
    
    with open(file_path, 'wb') as f:
      image.save(f, 'JPEG')
      
    print('Success.')
  except Exception as e:
    print('Failed - ', e)
  
urls = getImages(wd, 2, 5)
print(urls)
wd.quit()