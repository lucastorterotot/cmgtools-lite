import pymongo 
import re 
import pprint
import copy

pwd_writer='MwriterO'
client1 = pymongo.MongoClient(
    'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
        'writer', pwd_writer, 'datasets_test'
        ),
    27017
    )

# orginal db from se
coll_test = client1['datasets_test']['se']

infos = list(coll_test.find())

def remove_duplicates(infos):
    '''removes duplicate infos. 
    
    if several infos have the same name, the one with the latest sub_date is kept.
    the ordering of the input list is preserved.
    '''
    by_name = dict()
    for info in infos:
        by_name.setdefault(info['name'], []).append(info)
    no_dupes = []
    for info in infos: 
        infos_with_this_name = by_name.get(info['name'], None)
        if infos_with_this_name is None: 
            # happens if latest info already added to no_dupes, 
            # see below
            continue
        ninfos = len(infos_with_this_name)
        if ninfos==1: 
            no_dupes.append(infos_with_this_name[0])
        else: 
            # using lexicographical comparison on sub_date. 
            # this assumes that sub_date is of the form: 
            # year month day hour min sec
            latest = max(infos_with_this_name, key=lambda x: x['write_date'])
            no_dupes.append(latest)
        # remove this name from the dictionary, 
        # so that the latest info is not added several times
        del by_name[info['name']]
    return no_dupes

no_dupes = remove_duplicates(infos)

print(len(infos), len(no_dupes))

# new db from submission dirs
# pwd_writer = raw_input('writer password:')
client2 = pymongo.MongoClient(
    'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
        'writer', 'MwriterO', 'datasets'
        ),
    27017
    )
coll = client2['datasets']['se']

for info in no_dupes:
    del info['_id']
    olddocs = list(coll.find({'name':info['name']}))
    if len(olddocs) != 1:
        print len(olddocs)
        for doc in olddocs:
            print(doc)
        continue
    newdoc = copy.deepcopy(olddocs[0])
    newdoc.update(info)
    if newdoc.get('path') is None: 
        import pdb; pdb.set_trace()
    # print('new')
    # pprint.pprint(newdoc)
    coll.replace_one({'name':info['name']}, newdoc)
    # docs =  list(coll.find({'name':info['name']}))
    #for doc in docs:
    #    if doc.get('path') is None:
    #        import pdb; pdb.set_trace()
    # print('replaced')
    # pprint.pprint(docs[0])
    # import pdb; pdb.set_trace()
    
