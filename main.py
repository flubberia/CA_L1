from lxml import html
import requests
import xml.etree.ElementTree as ET
import time

class Bank:
    def __init__(self, name, url, buy, sale):
        self.url = url
        self.buy = buy
        self.sale = sale
        self.name = name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Money:
    def __init__(self, buy, sale):
        self.buy = buy
        self.sale = sale

    def __eq__(self, other):
        return (self.buy == other.buy) & (self.sale == other.sale)

def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    banks = []
    for bank in root.findall('bank'):
        banks.append(Bank(bank.attrib['name'], bank.find('url').text, bank.find('buy').text, bank.find('sale').text))
    return banks

class responce:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def get_data_from_url(bank, test=False):
    page = responce
    if test:
        page.status_code = 200
        file = open('test.html', 'r')
        page.text = file.read()
        file.close()
    else:
        page = requests.get(bank.url)
    if page.status_code != requests.HTTPError:
        if page.text.encode("utf-8") != '':
            tree = html.fromstring(page.text.encode("utf-8"))
            buy = tree.xpath('%s/text()' % bank.buy)
            sale = tree.xpath('%s/text()' % bank.sale)
            if (buy != []) & (sale != []):
                return Money(buy[0], sale[0])
    return Money("0", "0")

def collect_money(banks):
    for bank in banks:
        data = get_data_from_url(bank)
        if data != Money("0", "0"):
            bank.money = data
    return banks

def do_job_with_money():
    banks = collect_money(parse_xml("input.1.xml"))
    root = ET.Element('result')
    buy = ET.SubElement(root, 'buy')
    sale = ET.SubElement(root, 'sale')
    for bank in banks:
        ET.SubElement(buy, 'bank', {'name': bank.name}).text = bank.money.buy
        ET.SubElement(sale, 'bank', {'name': bank.name}).text = bank.money.sale
    ET.ElementTree(root).write("output.xml", 'utf-8')

def execute():
    begin = time.time()
    do_job_with_money()
    print('Time: %s' % (time.time() - begin))

execute()