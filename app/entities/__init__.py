import pony.orm as pny

import datetime


db = pny.Database()
now = datetime.datetime.now()


def setup_db(live):

    # if live == True (production) use the configuration
    # parameters to connect to Heroku
    if live:
        print('Using Heroku db configuration')
        db.bind(provider='postgres', user='xwyxzxdycdgwjr',
                password='17d7f9b3adf93fb172231983bab78bf20aa3ec49cf9f1e837fa3358339a6d289',
                host='ec2-107-20-193-206.compute-1.amazonaws.com', database='dcd3stjdjv6j65')

    else:
        print('Using localhost db configuration')
        db.bind(provider='postgres', user='postgres', password='syril',
                host='localhost', database='test')

    db.generate_mapping(create_tables=False)
