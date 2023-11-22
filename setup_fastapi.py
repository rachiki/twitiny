from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_models import User, Twit, Follow, Like

# Initialize FastAPI application
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# User authentication routes
@app.post("/signup/")
def signup(user: User):
    if any(u['username'] == user.username for u in users_db):
        raise HTTPException(status_code=400, detail="Username already taken")
    users_db.append(user.dict())
    return {"message": "User created successfully"}

@app.post("/login/")
def login(user: User):
    if user.dict() in users_db:
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/logout/")
def logout():
    # Placeholder for logout logic
    return {"message": "Logout successful"}

# Tweet routes
@app.post("/tweet/")
def post_tweet(tweet: Tweet):
    tweets_db.append(tweet.dict())
    return {"message": "Tweet posted successfully"}

@app.get("/tweets/", response_model=List[Tweet])
def get_tweets():
    return tweets_db

@app.delete("/tweet/{tweet_id}")
def delete_tweet(tweet_id: int):
    if tweet_id >= len(tweets_db) or tweet_id < 0:
        raise HTTPException(status_code=404, detail="Tweet not found")
    del tweets_db[tweet_id]
    return {"message": "Tweet deleted successfully"}

# Followers routes
@app.post("/follow/{username}")
def follow_user(username: str):
    follows_db.append(username)
    return {"message": f"Now following {username}"}

@app.post("/unfollow/{username}")
def unfollow_user(username: str):
    if username in follows_db:
        follows_db.remove(username)
        return {"message": f"Unfollowed {username}"}
    return {"message": "User not followed"}

# Likes routes
@app.post("/like/{tweet_id}")
def like_tweet(tweet_id: int):
    likes_db.append(tweet_id)
    return {"message": "Tweet liked"}

@app.post("/unlike/{tweet_id}")
def unlike_tweet(tweet_id: int):
    if tweet_id in likes_db:
        likes_db.remove(tweet_id)
        return {"message": "Tweet unliked"}
    return {"message": "Tweet not liked"}