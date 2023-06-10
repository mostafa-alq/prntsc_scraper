import os
fileName = 'C:\Zone\code\Webscraping\scrapedImages\IIb7oYCLRfOb5vf8955LwA.jpeg'
fileStats = os.stat(fileName)

print(fileStats)
print(f'File size in bytes is {fileStats.st_size}')
print(f'File size in megabytes is {fileStats.st_size / (1024 * 1024)}')