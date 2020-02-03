# coding: utf-8
# Импортирует поддержку UTF-8.
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

todos = {}

parser = reqparse.RequestParser()
parser.add_argument('uid')


class TodoSimple(Resource):
    def get(self):
        args = parser.parse_args()
        return {args: uid}

    # def put(self, todo_id):
    #     todos[todo_id] = request.form['data']
    #     return {todo_id: todos[todo_id]}


api.add_resource(TodoSimple, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
