# /bin/python3
import sys
import json
import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

def get_data(filename):
    with open(filename) as json_data:
        result = json.load(json_data)
    return result

def build_abstract(ia):
    ii = ia.get('InvertedIndex', {})
    lst = [' '] * ia.get('IndexLength', 0)
    for word in ii.keys():
        positions = ii.get(word)
        for pos in positions:
            lst[pos] = word
    return ' '.join(lst)

if __name__ == '__main__':
    mypath = sys.argv[1] if len(sys.argv) > 1 else ''
    if not isdir(mypath):
        print('Provide path to directory containing .json files')
        exit(-1)

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    rows = []
    for filename in onlyfiles:
        print('processing %s...' % filename)
        filepath = mypath + '/' + filename
        data = get_data(filepath)
        entities = data.get('entities', [])
        for entity in entities:
            if entity.get('IA') and not entity.get('A*'):
                entity.setdefault('A*', build_abstract(entity.get('IA')))
            sources = entity.get('S', [])
            first_source = sources[0].get('U') if len(sources) > 0 else None
            author_names = [ a.get('AuN') for a in entity.get('AA', []) ]
            field_names = [ field.get('DFN') for field in entity.get('F', []) ]
            rows.append({
                'Id': entity.get('Id'),
                'Title': entity.get('Ti'),
                'Year': entity.get('Y'),
                'CitationsCount': entity.get('CC'),
                'FirstSource': first_source,
                'AuthorsCount': len(author_names),
                'Authors': ', '.join(author_names),
                'Abstract': entity.get('A*', ''),
                'Topics': ', '.join(field_names)
            })
        # with open(filepath, "w") as json_data:
        #     json.dump(data, json_data)
        #     print('done')
    df = pd.DataFrame(rows)
    df.drop_duplicates('Id', inplace=True)
    # TODO: sort columns
    # TODO: remove index
    df.to_csv('out.csv')
