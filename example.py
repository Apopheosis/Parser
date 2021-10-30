import requests
from bs4 import BeautifulSoup
import csv
import xlsxwriter

n=6
amount=0

workbook = xlsxwriter.Workbook('parsed.csv')
worksheet = workbook.add_worksheet()


for i in range(n):

    row = 0
    col = 0
    worksheet.write_row(row, col, ('ID','URI','Brand','Name','Price'))
    row+=1

    page = '&page=' + str(i+1)
    req = requests.get("https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki?sort=popular"+page)

    print('================== Страница: ' + str(i+1) + ' ==================')

    soup = BeautifulSoup(req.text, 'lxml')

    links = soup.find_all('div', 'product-card j-card-item')
    amount += len(links)
    #fieldnames = ['ID','Link','Brand','Name','Price']
    for link in links:
            uri = 'https://wildberries.ru' + link.find('a', 'product-card__main j-open-full-product-card')['href']
            gid = link.find('a', 'product-card__main j-open-full-product-card')['href'][len('/catalog/'):]
            gid = gid[:7]
            brand = link.find('strong', 'brand-name').contents[0]
            name = link.find('span','goods-name').contents[0]


            try:
                price = link.find('span', 'price-commission__current-price').contents[0]
            except(AttributeError):
                price = link.find('span', 'lower-price').contents[0]
            data = (gid, uri, brand, name, price)
            worksheet.write_row(row, col, data)

            row += 1
    if (i+1!=6):
        worksheet = workbook.add_worksheet()

workbook.close()
print(amount)


