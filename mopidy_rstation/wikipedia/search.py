import sys
import wikipedia


def do(query, lang):
    wikipedia.set_lang(lang)
    # ret = wikipedia.page(query).summary
    ret = wikipedia.page(query).summary + ' ' + wikipedia.page(query).content
    # print(ret.original_title)
    return ret


def main():
    query = "test"
    if len(sys.argv) > 1:
        query = sys.argv[1]
    print(do(query, 'pl'))

if __name__ == '__main__':
    main()
    sys.exit()
