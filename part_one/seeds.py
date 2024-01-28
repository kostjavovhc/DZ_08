from models import Author, Quote
import json
from mongoengine.errors import NotUniqueError

if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for i in data:
            try:
                author = Author(fullname=i.get('fullname'), 
                            born_date=i.get('born_date'),
                            born_location=i.get('born_location'),
                            description=i.get('description'))
                author.save()
            except NotUniqueError as e:
                print(f'Author already exists: {i.get("fullname")}')

    with open('qoutes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for i in data:
            author, *_ = Author.objects(fullname=i.get('author'))
            quote = Quote(quote=i.get('quote'), tags=i.get('tags'), author=author)
            quote.save()

