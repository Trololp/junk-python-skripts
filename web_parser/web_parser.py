from bs4 import BeautifulSoup
import requests
import xlsxwriter

# establishing session
s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
})


def load_page(page, session):
    url = 'http://vixim.ru/new-torrent/%d.html?pages=50' % (page)
    print(url)
    request = session.get(url)
    return request.text


def read_file(filename):
    with open(filename, 'rb') as input_file:
        text = input_file.read()
    return text


def parse_user_datafile_bs(filename):
    results = []
    print(f"parsing : {filename}")
    text = read_file(filename)

    soup = BeautifulSoup(text, features="html.parser")
    film_list = film_list = soup.find('div', {'class': 'film-list'})
    items = film_list.find_all('div', {'class': 'film-item'})
    for item in items:
        # getting movie name and link
        movie_link = item.find('div', {'class': 'film-image'}).find('a').get('href')
        movie_name = item.find('h2').text
        print(f"film: {movie_name}")
        # getting scores
        movie_info = item.find('div', {'class': 'film-info'})
        recomend_count = movie_info.find('span', {'class': 'recommend_count'}).text
        movie_score = movie_info.find('em', {'class': 'inline-rating'}).get('average')
        movie_votes = movie_info.find('em', {'class': 'inline-rating'}).get('votes')
        recomend_count = recomend_count[-2:]
        if recomend_count:
            recomend_count = int(recomend_count)
        if movie_score:
            movie_score = float(movie_score)
        if movie_votes:
            movie_votes = int(movie_votes)

        # getting genre, tags and etc...
        tags = ''
        genre_info = item.find('div', {'class': 'film-genre'})
        genre_tags = genre_info.find('div').text
        tag_list = genre_info.find('div', {'class': 'tag_list'})
        if tag_list is None:
            tags = 'No tags'
        else:
            for tag_info in tag_list.find_all('a'):
                tags = tags + tag_info.text[3:] + ' '

        results.append({
            'name': movie_name,
            'link': 'http://vixim.ru' + movie_link,
            'score': movie_score,
            'votes': movie_votes,
            'recomends': recomend_count,
            'genre': genre_tags,
            'tags': tags
        })
    return results


# loading files
last_page = 922

for page in range(last_page):
    data = load_page(page, s)
    with open('./page_%d.html' % (page), 'wb') as output_file:
        output_file.write(data.encode('utf-8'))

# parsing
workbook = xlsxwriter.Workbook('filmi.xlsx')
worksheet = workbook.add_worksheet()

counts = 1
for page in range(last_page):
    results = parse_user_datafile_bs('./page_%d.html' % page)
    for result in results:
        worksheet.write(counts, 0, result['name'])
        worksheet.write(counts, 1, result['score'])
        worksheet.write(counts, 2, result['votes'])
        worksheet.write(counts, 3, result['recomends'])
        worksheet.write(counts, 4, result['link'])
        worksheet.write(counts, 5, result['score'] * result['votes'])
        worksheet.write(counts, 6, result['genre'])
        worksheet.write(counts, 7, result['tags'])
        counts = counts + 1

workbook.close()
