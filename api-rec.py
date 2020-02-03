# coding: utf-8
# Импортирует поддержку UTF-8.
from flask import Flask
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api(app)

ai_quotes = [
    {
        "id": 0,
        "author": "Kevin Kelly",
        "quote": "The business plans of the next 10,000 startups are easy to forecast: " +
                 "Take X and add AI."
    },
    {
        "id": 1,
        "author": "Stephen Hawking",
        "quote": "The development of full artificial intelligence could " +
                 "spell the end of the human race… " +
                 "It would take off on its own, and re-design " +
                 "itself at an ever increasing rate. " +
                 "Humans, who are limited by slow biological evolution, " +
                 "couldn't compete, and would be superseded."
    },
    {
        "id": 2,
        "author": "Claude Shannon",
        "quote": "I visualize a time when we will be to robots what " +
                 "dogs are to humans, " +
                 "and I’m rooting for the machines."
    },
    {
        "id": 3,
        "author": "Elon Musk",
        "quote": "The pace of progress in artificial intelligence " +
                 "(I’m not referring to narrow AI) " +
                 "is incredibly fast. Unless you have direct " +
                 "exposure to groups like Deepmind, " +
                 "you have no idea how fast — it is growing " +
                 "at a pace close to exponential. " +
                 "The risk of something seriously dangerous " +
                 "happening is in the five-year timeframe." +
                 "10 years at most."
    },
    {
        "id": 4,
        "author": "Geoffrey Hinton",
        "quote": "I have always been convinced that the only way " +
                 "to get artificial intelligence to work " +
                 "is to do the computation in a way similar to the human brain. " +
                 "That is the goal I have been pursuing. We are making progress, " +
                 "though we still have lots to learn about " +
                 "how the brain actually works."
    },
    {
        "id": 5,
        "author": "Pedro Domingos",
        "quote": "People worry that computers will " +
                 "get too smart and take over the world, " +
                 "but the real problem is that they're too stupid " +
                 "and they've already taken over the world."
    },
    {
        "id": 6,
        "author": "Alan Turing",
        "quote": "It seems probable that once the machine thinking " +
                 "method had started, it would not take long " +
                 "to outstrip our feeble powers… " +
                 "They would be able to converse " +
                 "with each other to sharpen their wits. " +
                 "At some stage therefore, we should " +
                 "have to expect the machines to take control."
    },
    {
        "id": 7,
        "author": "Ray Kurzweil",
        "quote": "Artificial intelligence will reach " +
                 "human levels by around 2029. " +
                 "Follow that out further to, say, 2045, " +
                 "we will have multiplied the intelligence, " +
                 "the human biological machine intelligence " +
                 "of our civilization a billion-fold."
    },
    {
        "id": 8,
        "author": "Sebastian Thrun",
        "quote": "Nobody phrases it this way, but I think " +
                 "that artificial intelligence " +
                 "is almost a humanities discipline. It's really an attempt " +
                 "to understand human intelligence and human cognition."
    },
    {
        "id": 9,
        "author": "Andrew Ng",
        "quote": "We're making this analogy that AI is the new electricity." +
                 "Electricity transformed industries: agriculture, " +
                 "transportation, communication, manufacturing."
    }
]


class Quote(Resource):
    def get(self, userid=0):
        if userid == 0:
            return 'Please send userid', 404
            # return random.choice(ai_quotes), 200
        else:
            # for quote in ai_quotes:
            #     if quote["id"] == id:
            #         return quote, 200
            # return "Quote not found", 404
            return recomended_for(userid), 200

    # def post(self, id):  # добавление
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("author")
    #     parser.add_argument("quote")
    #     params = parser.parse_args()
    #     for quote in ai_quotes:
    #         if id == quote["id"]:
    #             return f"Quote with id {id} already exists", 400
    #     quote = {
    #         "id": int(id),
    #         "author": params["author"],
    #         "quote": params["quote"]
    #     }
    #     ai_quotes.append(quote)
    #     return quote, 201
    #
    # def put(self, id):  # изменения
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("author")
    #     parser.add_argument("quote")
    #     params = parser.parse_args()
    #     for quote in ai_quotes:
    #         if (id == quote["id"]):
    #             quote["author"] = params["author"]
    #             quote["quote"] = params["quote"]
    #             return quote, 200
    #
    #     quote = {
    #         "id": id,
    #         "author": params["author"],
    #         "quote": params["quote"]
    #     }
    #
    #     ai_quotes.append(quote)
    #     return quote, 201
    #
    # def delete(self, id):
    #     global ai_quotes
    #     ai_quotes = [qoute for qoute in ai_quotes if qoute["id"] != id]
    #     return f"Quote with id {id} is deleted.", 200


def delete_index(name_index):
    # ТОЛЬКО ДЛЯ УДАЛЕНИЯ
    es.indices.delete(index=name_index, ignore=400)


def new_index(name_index):
    # mapping dictionary that contains the settings and
    # _mapping schema for a new Elasticsearch index:
    mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "userId": {
                    "type": "integer"  # formerly "string"
                },
                "date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "cId": {
                    "type": "integer"
                },
                "action": {
                    "type": "text"
                },
                "fids": {
                    "type": "text"
                }
            }
        }
    }

    # ТОЛЬКО ДЛЯ СОЗДАНИЯ
    # create an index in elasticsearch, ignore status code 400 (index already exists)
    es.indices.create(index=name_index, body=mapping)
    #    {'acknowledged': True, 'shards_acknowledged': True, 'index': 'my-index'}


def info_index(name_index):  # get info about index
    es.indices.get_mapping(index=name_index)


def load_info():
    f = open('treto01.json')
    data = json.loads(f.read())
    dict_for_downloads = {i: data[i] for i in range(0, len(data))}
    for id, item in dict_for_downloads.items():
        item['fids'] = str(item['fids'])
    for id, item in dict_for_downloads.items():
        es.index(index="events", id=id, doc_type='_doc', body=item)
    #     if id > 2:
    #         break


def search_fids(fids, userId):
    res = es.search(index="events",
                    body={
                        "size": 10,
                        "_source": ["cId"],
                        "sort": [{"date": "desc"}],
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                        "multi_match": {
                                            "query": fids,
                                            "fields": ["fids"]
                                        }
                                    }
                                ],
                                "must_not": [
                                    {
                                        "multi_match": {
                                            "query": userId,
                                            "fields": ["userId"]
                                        }
                                    }
                                ]
                            }
                        },
                        "collapse": {
                            "field": "cId"
                        }
                    })
    a1 = {}
    for i in range(0, len(res['hits']['hits'])):
        a1[i] = res['hits']['hits'][i]['_source']['cId']
    res = json.dumps(a1)
    return res
    # 'treto01.json'


def search_tags_from_userId(userId):
    res = es.search(index="events",
                    body={
                        "size": 44,
                        "_source": ["userId", "fids"],
                        "sort": [{"date": "desc"}],
                        "query": {
                            "term": {
                                'userId': userId,
                            }
                        }
                    }
                    )
    return res


def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c, '')
    return value;


def user_preffers(userId):
    res = search_tags_from_userId(userId)
    a = ''
    for i in range(0, len(res['hits']['hits'])):
        a = a + res['hits']['hits'][i]['_source']['fids'] + ' '
    a = remove(a, '\,/:*?"<[]>|')
    counts = Counter(a.split(' ')[:-1])
    d = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    output = []
    for k in d:
        if k not in output:
            output.append(k)
            if len(output) == 10:
                break
    return output


def recomended_for(userId):
    preffer = user_preffers(userId)
    res_fids = search_fids(preffer, userId)
    return res_fids


# api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")
api.add_resource(Quote, "/recc", "/recc/", "/recc/<int:userid>")
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
