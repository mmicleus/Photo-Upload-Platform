from fastapi import FastAPI,HTTPException,File,UploadFile,Form,Depends
from app.schemas import PostCreate , PostReturn
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

#this function will run automatically when the application starts and will create the database and tables if they don't exist.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield   

app = FastAPI(lifespan=lifespan)



#creates a new post in the database with the provided caption and file information when the file is uploaded.

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy url", 
        fileType="photo",
        file_name="dummy name" # Replace with actual URL after saving the file
    )

    #add post to database
    session.add(post)
    await session.commit()
    await session.refresh(post)

    return post


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))

    posts = [row[0] for row in result.all()]

    posts_data = []

    for post in posts:
      posts_data.append({
          "id": str(post.id),
          "caption": post.caption,
          "url": post.url,
          "file_type": post.fileType,
          "file_name": post.file_name,
          "created_at": post.created_at.isoformat()
      })  


    return {"posts": posts_data}































# @app.get("/posts")
# def get_all_posts(limit: int = None):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts


# @app.get("/posts/{id}")
# def get_post(id: int) -> PostReturn:
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return text_posts.get(id)


# @app.post("/posts")
# def create_post(post: PostCreate) -> PostReturn:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post

#     return new_post








