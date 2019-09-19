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

info_pattern = re.compile(r'.*(\d{6})/(.*)/(.*)/(.*)$')
for i,info in enumerate(infos): 
    m = info_pattern.match(info['path'])
    if not m: 
        print('no match')
        continue
    prod_date, sample_version, sample, write_date = m.groups()
    name =  '{}%{}%{}'.format(
        prod_date, sample, sample_version
        )
    info['name'] = name
    info['prod_date'] = prod_date
    info['sample_version'] = sample_version
    info['sample'] = sample
    info['write_date'] = write_date
    del info['_id']    
    olddocs = list(coll_test.find({'path':info['path']}))
    if len(olddocs) != 1:
        print len(olddocs)
        for doc in olddocs:
            print(doc)
        continue
    newdoc = copy.deepcopy(olddocs[0])
    newdoc.update(info)
    if newdoc.get('path') is None: 
        import pdb; pdb.set_trace()
#    print('new')
#    pprint.pprint(newdoc)
    # import pdb; pdb.set_trace()

    coll_test.replace_one({'path':info['path']}, newdoc)
    # docs =  list(coll.find({'name':info['name']}))
    # for doc in docs:
    #     if doc.get('path') is None:
    #         import pdb; pdb.set_trace()
    # print('replaced')
    # pprint.pprint(docs[0])
    # import pdb; pdb.set_trace()
    
