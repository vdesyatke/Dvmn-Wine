from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
from auxiliary_functions import decline_years
import pandas as pd


FOUNDATION_YEAR = 1920


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    age_of_winery = date.today().year - FOUNDATION_YEAR
    age_of_winery = decline_years(age_of_winery)

    wines_df = pd.read_excel(
        'wine3.xlsx',
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
