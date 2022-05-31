import tkinter

from bs4 import BeautifulSoup
import requests
import csv
import argparse
import logging
import os
import sys
from datetime import datetime

LOG_LEVEL = os.environ.get('LOGGING', 'INFO').upper()

logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL,
    style='{',
    format="{asctime} {levelname} {name} {threadName} : {message}")

lgr = logging.getLogger(__name__)


def extract_products(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    lgr.debug(soup)
    ul = soup.find("ul", {"class": ["block-grid", "columns4", "collection-th"]})
    lgr.debug(ul)

    products = []

    for li in ul.find_all('li'):
        # lgr.info(link.get('href'))

        lgr.debug('# -----------------------------')
        lgr.debug(li)
        lgr.debug('# -----------------------------')

        # Get product title span
        product_title_span = li.find("span", {"class": "product-title"})
        # Get Product name - span text content
        product_name = product_title_span.findAll(text=True, recursive=False)[0]

        # Get span in Product name
        product_cost_span = product_title_span.find("span", {"class": "money"})
        product_cost = product_cost_span.text

        lgr.info('# NEW PRODUCT -----------------------------')
        lgr.info(f'Name: {product_name}')
        lgr.info(f'Cost: {product_cost}')
        lgr.info('# -----------------------------')

        # data = f"# NEW PRODUCT ------------------\nName: {product_name}\nCost: {product_cost}"
        list_box.insert(END, '# NEW PRODUCT ------------------')
        list_box.insert(END, f'Name: {product_name}')
        list_box.insert(END, f'Cost: {product_cost}')
        list_box.insert(END, '#---------------------')
        list_box.update()
        products.append([product_name, product_cost])

    return products


def main(start, max_pages):
    # url = 'https://sharkrobot.com/collections/vivziepop'
    more_pages_exist = True
    page = 0

    now = datetime.now()  # current date and time
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")

    with open(f'sharkrobot-scrape-{date_time}.csv', 'w') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(['name', 'cost'])

        while more_pages_exist:
            page += 1
            url = f'{start}?page={page}'
            lgr.info(f'Loading page: {url}')
            response = requests.get(url)
            lgr.info(response)
            print(page)
            bar['value'] = (page / max_pages)*100
            bar.update()
            products = extract_products(response.text)
            writer.writerows(products)

            if len(products) == 0 or page >= max_pages:
                bar['value'] = 100
                lgr.info('Completed')
                list_box.insert(END, 'Completed')
                break


if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(description='Sharkrobot scrapper.')
    parser.add_argument('--start', help='Start Url', required=True)
    parser.add_argument('--pages', help='Limit of Pages to Process', type=int)
    parser.add_argument('--output', help='List box')
    args = parser.parse_args()
    result_data=[]
    '''
    from tkinter import *
    from tkinter import ttk, messagebox

    font_name = 'Arial'
    font_size = 16
    font = (font_name, font_size, 'bold')
    root = Tk()
    root.title("Scrapping")
    root.geometry('400x600')

    Label(root, text='Scraping Product Tool', font=(font_name, font_size + 8, 'bold')).pack(pady=30)

    Label(root, text='Enter Website URL', font=font).pack()
    entry_url = Entry(root, width=35, font=(font_name, font_size))
    entry_url.pack(pady=(2, 10))

    Label(root, text='Enter Number of pages', font=font).pack()
    entry_pages = Entry(root, width=25, font=(font_name, font_size), justify=CENTER)
    entry_pages.pack(pady=(2, 30))

    Label(root, text='Enter Variables', font=font).pack()
    list_box = Listbox(root, width=45)
    list_box.pack()
    url = 'https://sharkrobot.com/collections/vivziepop'

    Button(root, text='Start', font=font, width=12, command=lambda: run()).pack(pady=20)

    bar = ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate')
    bar.pack(side=BOTTOM, fill=X, expand=True)
    pages = 0


    def run():
        bar['value']=0
        list_box.delete(0, END)
        try:
            pages = int(entry_pages.get())
            print(pages)
            bar.config(length=pages)
        except ValueError:
            messagebox.showwarning('Error:', 'Enter Valid number of pages')
        web_url = entry_url.get()
        print(web_url)
        main(web_url, pages)


    root.mainloop()
