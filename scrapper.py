import requests
import lxml.html as html
import os 
import datetime

XPATH_LINK_TO_ARTICLE = '//div[@class="news V_Title_Img"]/a/@href'
# obtener titulos
XPATH_TITLE = '//h1[@class]/i/text()'
# obtener resumen
XPATH_SUMMARY = '//div[@class="lead"]/p[not(@class)]/text()'    
# obtener noticia
XPATH_NOTICE = '//div[@class="html-content"]/p[not(@class)]/text()'
# obtener Autor
XPATH_AUTHOR = '//div[@class="autorArticle"]/p/text()'
HOME_URL = 'https://www.larepublica.co/'

def parse_notice(link, today):
    try:
        response =  requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('        ','').replace('\n','').replace('\"','')
                author = parsed.xpath(XPATH_AUTHOR)[0]
                author = author.replace('\n','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_NOTICE)
                print(title)
            except IndexError as e:
                return
            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n')
                f.write(author)
                f.write('\n')
                f.write(summary)
                f.write('\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
                f.close()
        else:
            raise ValueError(f'ERROR: {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links2notice = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links2notice:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == "__main__":
    run()
