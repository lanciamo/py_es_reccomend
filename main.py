# coding: utf-8
# Импортирует поддержку UTF-8.

import json
from elasticsearch import Elasticsearch
from collections import Counter

# by default we connect to localhost:9200
es = Elasticsearch()


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


def menu():
    action = input(
        "And what do you want?\n Choose:\n[1] Искать fids по userId\n[2] Искать cId по "
        "fids and user_id\n "
        "[3] Combo!!! cIDs on user_id - now! \n[4] Drop current DataBase\n[5] Exit\n")

    if action == "1":
        user_id = input("Input user_id: ")  # python
        # page_num = int(input("For how many pages do you want go deeper : "))  # 2
        # parse_hh(position, page_num, collection, mode="all")
        print(user_preffers(user_id))
    elif action == "2":
        user_id = input("Input user_id: ")  # python
        fids = input("Input list of fids : ")
        # parse_hh(position, page_num, collection, mode="update")
        print(search_fids(fids, user_id))
    elif action == "3":
        user_id = input("Input user_id: ")  # python
        fids = input("Input list of fids : ")
        print(recomended_for(fids, user_id))
    elif action == "4":
        collection.drop()
    elif action == "5":
        return False


while __name__ == "__main__":
    if not menu():
        break
