from typing import Optional
from fastapi import FastAPI , status , Response ,HTTPException
from fastapi.params import Body
from random import randrange
from pydantic import BaseModel

app = FastAPI()

class post(BaseModel):
    title:str
    content:str
    publisher:bool=True
    rating :Optional[int]=None

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
    return {"data":my_posts}


# @app.post("/create_posts")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post":f"title: {payload['title']}, content: {payload['content']}"}

@app.post("/posts" ,status_code = status.HTTP_201_CREATED)
async def create_post(post : post):
    post_dict =post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data" :post_dict}


# @app.get("/posts/{id}")
# async def get_post(id):
#     print(id)
#     return {"data" :my_posts[int(id)]}

@app.get ("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1 ]
    return {"data" : post}  

@app.get("/posts/{id}")
async def get_post(id : int):
    post = find_post(id)
    if post ==None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    return {"data" : post}


@app.delete("/posts/{id}", status_code =status.HTTP_204_NO_CONTENT)
async def delete_post(id : int):
    index = find_index(id)
    if index ==None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id : int , post :post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    post_dict = post.dict()
    post_dict["id"]=id
    my_posts[index]=post_dict
    return {"data":post_dict}
