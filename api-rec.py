# coding: utf-8
# Импортирует поддержку UTF-8.
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
from elasticsearch import Elasticsearch
from collections import Counter

# by default we connect to localhost:9200
es = Elasticsearch()
app = Flask(__name__)
api = Api(app)

queries = {}


class Recommend(Resource):
    def get(self, user_id):
        # return {"id": user_id}
        return recomended_for(user_id)

    def put(self, user_id):
        queries[user_id] = request.form['data']
        return {queries: queries[user_id]}


def delete_index(name_index):  # ТОЛЬКО ДЛЯ УДАЛЕНИЯ
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


def search_tags_from_userId(userId):
    res = es.search(index="events",
                    body={
                        "size": 100,
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
    return value


def most_popular_fids():
    res = es.search(index="events",
                    body={
                        "size": 1000,
                        "_source": ["fids"],
                        "sort": [{"date": "desc"}]
                    }
                    )
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


def user_preffers(userId):
    res = search_tags_from_userId(userId)
    if len(res['hits']['hits']) == 0:
        mpf = most_popular_fids()
        return mpf
    else:
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
    res_fids = search_fids(str(preffer), userId)
    return res_fids


api.add_resource(Recommend, '/<string:user_id>')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
