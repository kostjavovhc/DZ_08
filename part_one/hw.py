import redis
from typing import List, Any
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)



@cache
def find_by_tag(tag:str) -> list[str|None]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]

    if result != []:
        return result
    else:
        return 'No matches'
@cache
def find_by_author(author:str) -> list[list[Any]]:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]

    if result != {}:
        return result
    else:
        return 'No matches'

@cache
def find_by_tags(tags_array:str):
    tags = tags_array.split(',')
    result = []
    for tag in tags:
        r = find_by_tag(tag)
        for q in r:
            if q not in result:
                result.append(q)

    if result != []:
        return result
    else:
        return 'No matches'


if __name__ == '__main__':

    while True:
        u_i = input('Write a command and param: ')
        if u_i[0] == 'exit':
            print('Goodbye!')
            break

        try:
            command, param = u_i.split(':')
        except ValueError:
            print('Wrong value')

        if command == 'name':
            r = find_by_author(param)

        elif command == 'tag':
            r = find_by_tag(param)

        elif command == 'tags':
            r = find_by_tags(param)

        else:
            r = 'Wrong Value'
            
        print(r)

