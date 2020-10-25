# Note on Mongodb query
* cli tools mongo
* mongo mongodb://$[hostlist]/$[database]?authSource=$[authSource] --username --p
* data save in JSON Document

## command
* use db
* show dbs
* show collections
* show users

* find or list db
```
 db.tweets.find( {} )
{ "_id" : ObjectId("5f92587c3be784b494887c83"), "body" : "New tweets", "id" : "18", "timestamp" : "2017-03-11T06:39:40Z", "tweetedby" : "testuser" }
```

* get help
    db.collection.help

* insert data (use inset_one, insert_many instead)
```
db.apirelease.insert ({
...                 "buildtime": "2017-01-01 10:00:00",
...                 "links": "/api/v1/users",
...                 "methods": "get, post, put, delete",
...                 "version": "v1"
...             })
WriteResult({ "nInserted" : 1 })
```

