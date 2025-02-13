# Novel to EPUB

import requests
from bs4 import BeautifulSoup
import time
from ebooklib import epub
import validators

main_url = 'https://www.royalroad.com'

def make_request(url):
    # Makes a request to get html data with python's request library
    for i in range(5):
        r = requests.get(url)
        if(r.status_code == requests.codes.ok):
            return BeautifulSoup(r.text, 'html.parser')    
        else:
            print(f'Status code {r.status_code}. Website rejected request. Waiting 5s before trying again.')
            time.sleep(5)             

def search(soup):
    # Searches royalroad for novel
    title = soup.find('h2', class_='fiction-title').find('a')
    link = soup.find('figure', class_='col-sm-2 col-md-3 col-lg-2 text-center').find('a')
    # return title and concatenated string
    return title.text, f'{main_url}{link.get('href')}' 
        
def fetch_title(soup):
    title_class = soup.find('h1', class_='font-white')
    title = title_class.text
    return title

def fetch_tags(soup):
    # Returns the novel's tags/genres 
    tags = 'Genres/Tags: '
    scraped_tags = soup.find_all('a', class_='label label-default label-sm bg-blue-dark fiction-tag')
    for tag in scraped_tags:
        tags += (f'{tag.text},')
    return tags

def fetch_author(soup):
    # Returns the novel's author
    author = soup.find('a', class_='font-white')
    return author.text

def fetch_description(soup, url):
    # returns novel description
    description = ''
    p_tags = soup.find('div', class_='hidden-content').find_all('p')
    for p in p_tags:
        description += f'<p>{p.text}</p>\n'
    description += f'\n\nScraped from {url}.'
    return description
    
def fetch_chapter_list(soup):
    # return list of chapters and their urls as dictionary 
    chapters_dictionary = []
    chapter_classes = soup.find_all('tr', class_='chapter-row')
    for chapter_class in chapter_classes:
        chapter = chapter_class.find('a')
        chapter_link = f'{main_url}{chapter.get('href')}'
        chapters_dictionary.append({'title': chapter.text.strip(), 'url': chapter_link})

    return chapters_dictionary

def fetch_chapters(chapter_list):
    # return chapter title and text data in a dictionary  
    chapters = []
    for chapter in chapter_list:
        print(f'Downloading {chapter['title']}')
        soup = make_request(chapter['url'])
        p_tags = soup.find_all('p')
        chapters.append({'title': chapter['title'], 'p_tags': p_tags})

    return chapters

def fetch_cover_image(soup):
    # return cover image
    image_link = soup.find('img', class_='thumbnail inline-block').get('src')
    image = requests.get(image_link).content
    return image

def pack_epub(chapters, author, cover, description, tags, book_title):
    # epub packing using ebooklib done here
    book = epub.EpubBook()
    # Add basic book data
    book.set_title(f'{book_title}')
    book.set_language('en')
    book.add_author(f'{author}')
    spine = ['nav']
    # Add css and style
    style = 'body { font-family: Times, Times New Roman, serif; }'
    nav_css = epub.EpubItem(uid='style_nav',
                file_name='style/nav.css',
                media_type='text/css',
                content=style)
    book.add_item(nav_css)
    # Create wrapped description
    wrapped_description = f'<html><body><h1>Introduction</h1><p>{description}</p></body></html>'
    # Create introduction item
    introduction = epub.EpubHtml(uid='Introduction', title='Introduction', file_name='intro.xhtml', lang='en')
    introduction.content = wrapped_description
    book.add_metadata('DC', 'description', f'{wrapped_description}')
    # Add it to the book
    book.add_item(introduction)
    spine.append(introduction)
    # Add tags/genres as metadata
    book.add_metadata('DC', 'subject', tags) 
    # Create and add cover
    cover_item = epub.EpubImage(uid='cover_image', file_name='cover.jpg', media_type='image/jpg', content=cover)
    book.add_item(cover_item)
    book.set_cover('book_cover.jpg', content=cover)
    chapter_object_list = [] 
    
    # Create chapter objects for each chapter. wrap text in html to meet epub standards
    for chapter in chapters:
        chapter_title = chapter['title']
        chapter_object = epub.EpubHtml(title=f'{chapter_title}', file_name=f'{chapter_title}.xhtml', lang='en')
        chapter_object.content = f'<h1>{chapter_title}</h1>'
        p_tags = chapter['p_tags']
        for p_tag in p_tags:
            chapter_object.content += f'<p>{p_tag.text}</p>\n' 

        book.add_item(chapter_object)
        chapter_object_list.append(chapter_object)
        spine.append(chapter_object)
        
    # Create and set table of contents + spine, add navigation
    book.toc = [epub.Link('intro.xhtml', 'Introduction', 'intro')] + chapter_object_list
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    epub.write_epub(f'{book_title}.epub', book)

def main():
    user_input = input('Please enter a novel title or url you wish to pack into an epub: ')
    if validators.url(user_input):
        book_url = user_input

    else:
        # Search for book on royalroad
        book_title, book_url = search(make_request(f'{main_url}/fictions/search?globalFilters=false&title={user_input}&orderBy=popularity'))
        user_decision = input(f'Is {book_title} ({book_url}) the novel you are looking for? Y/N: ')
        if(user_decision == 'N'):
            print('Try re-entering the title in a more complete manner. (ex. mother -> mother of learning) or entering the url directly.')
            return 0
    
    # Get soup for functions.
    soup = make_request(book_url)
    pack_epub(fetch_chapters(fetch_chapter_list(soup)), fetch_author(soup), fetch_cover_image(soup), fetch_description(soup, book_url), fetch_tags(soup), fetch_title(soup))


if __name__ == '__main__':
    main()