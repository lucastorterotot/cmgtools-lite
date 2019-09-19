import pymongo 
import re 
import pprint
import copy

pwd_reader='MreaderO'
pwd_writer='MwriterO'
# pwd_reader = raw_input('reader password:')
client1 = pymongo.MongoClient(
    'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
        'reader', pwd_reader, 'datasets_test'
        ),
    27017
    )

# orginal db from se
coll_test = client1['datasets_test']['se']

infos = list(coll_test.find())

# new db from submission dirs
# pwd_writer = raw_input('writer password:')
client2 = pymongo.MongoClient(
    'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
        'writer', pwd_writer, 'datasets'
        ),
    27017
    )
coll = client2['datasets']['se']

print('ninfos', len(infos))
pprint.pprint(infos[1])

for info in infos:
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
    
