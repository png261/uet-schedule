from bs4 import BeautifulSoup

def periodToTime(tiet):
    data  = tiet.split('-')
    start = '{:02d}:00'.format(int(data[0]) + 6)
    end = '{:02d}:50'.format(int(data[1]) + 6)
    return {'start':f'{start}', 'end': f'{end}'}

def tableToData(soup, headers=None, indent=None):
    rows = soup.find_all("tr")

    if not headers:
        headers = {}
        thead=soup.find("thead")

        if thead:
            thead = thead.find_all("th")
            for i in range(len(thead)):
                headers[i] = thead[i].text.strip().lower()

    data = []
    for row in rows:
        cells = row.find_all("td")
        if headers:
            items = {}
            if len(cells) > 0:
                for index in headers:
                    items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        if items:
            data.append(items)
    return data

