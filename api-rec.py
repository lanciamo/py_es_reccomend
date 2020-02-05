# coding: utf-8
# Импортирует поддержку UTF-8.
from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
import json
from elasticsearch import Elasticsearch
from collections import Counter

# by default we connect to localhost:9200
es = Elasticsearch()
app = Flask(__name__)
api = Api(app)

queries = {}

parser = reqparse.RequestParser()
parser.add_argument('uid')


class Events(Resource):
    def get(self):
        args = parser.parse_args()
        return recomended_for(args['uid']), 201

    def post(self):
        args = parser.parse_args()
        return recomended_for(args['uid']), 201


# ==================


def search_fids(fids, userId):
    res = es.search(index="events",
                    body={
                        "size": 10,
                        "_source": ["cId"],
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                        "match": {
                                            "fids": fids
                                        }
                                    }
                                ],
                                "must_not": [
                                    {
                                        "term": {
                                            "userId": userId
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


def list_to_txt(lis):
    b = ''
    for i in range(0, len(lis)):
        b = b + str(lis[i]) + ' '
    b = remove(b, '\,/:*?"<[]>|')
    return b


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
    #     a = remove(a, '\,/:*?"<[]>|')
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
        #         a = remove(a, '\,/:*?"<[]>|')
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
    preffer = list_to_txt(preffer)
    res_fids = search_fids(preffer, userId)
    return res_fids


api.add_resource(Events, '/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
