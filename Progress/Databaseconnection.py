import os
from typing import Optional
from fastapi import FastAPI , status , Response ,HTTPException
from fastapi.params import Body
from random import randrange
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

class post(BaseModel):
    title:str
    content:str
    publisher:bool=True
    rating : Optional[int]=None

#Connecting Database
while True:
    try:
        conn = psycopg2.connect(host= 'localhost',database='Fastapi',user='postgres',
        password='Ashumylove',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection successful")
        break
    except Exception as error:
        print("database connection fail")
        print(error)


my_posts=[{"title":"post1","content":"content1","publisher":True,"rating":5,"id":1},{"title":"post2","content":"content2","publisher":True,"rating":4,"id":2},{"title":"post3","content":"content3","publisher":True,"rating":3,"id":3}]

@app.get("/")
def read_root():
    return {"welcome to my api!!!!"}


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

def find_index(id):
    for index , post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None

@app.get("/posts")
async def get_post():

    cursor.execute('SELECT * FROM "Post"')
    posts = cursor.fetchall()

    return {"data": posts}



@app.post("/posts" ,status_code = status.HTTP_201_CREATED)
async def create_post(post : post):

    cursor.execute("""INSERT INTO "Post" ("Title","content","publisher","rating") 
                    VALUES(%s,%s,%s,%s) RETURNING *""",(post.title,post.content,post.publisher,post.rating))
    conn.commit()
    new_post=cursor.fetchone()
    return {"data":new_post}


@app.get ("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1 ]
    return {"data": post}  

@app.get("/posts/{id}")
async def get_post(id : int):
    cursor.execute("""SELECT * FROM  "Post" WHERE "id"=%s""",(id,))
    post = cursor.fetchone()
    if post ==None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    print(post)
    return {"data": post}


@app.delete("/posts/{id}", status_code =status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):
    cursor.execute("""Delete from "Post" where "id"=%s""",(id,))
    conn.commit()
    delete_post = cursor.fetchone()
    if delete_post ==None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
async def update_post(id: int, Post: post):
    cursor.execute("""UPDATE "Post" SET "Title"=%s,"content"=%s,"publisher"=%s,"rating"=%s WHERE "id"=%s RETURNING *""" , 
    (Post.title,Post.content,Post.publisher,Post.rating,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    return {"data": updated_post}
