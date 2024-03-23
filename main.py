from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
from auxiliary_functions import decline_years
import pandas as pd
import argparse


FOUNDATION_YEAR = 1920


def create_parser():
    description = '''Сайт магазина авторского вина "Новое русское вино".'''
    parser = argparse.ArgumentParser(description=description)
    h = 'Путь к xlsx-файлу с базой данных продукции'
    parser.add_argument('-f', '--xls_file', help=h, default='wine3.xlsx')
    return parser


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    parser = create_parser()
    xls_file = parser.parse_args().xls_file

    template = env.get_template('template.html')

    age_of_winery = date.today().year - FOUNDATION_YEAR
    age_of_winery = decline_years(age_of_winery)

    wines_df = pd.read_excel(
        xls_file,
        na_values='None',
        keep_default_na=False,
    )

    wines = dict()
    for category in wines_df['Категория'].unique():
        df = wines_df[wines_df['Категория'] == category]\
            .drop(columns=['Категория'])
        wines[category] = df.to_dict(orient='records')

    rendered_page = template.render(
        age_of_winery=age_of_winery,
        wines=wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
