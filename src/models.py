from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    profile_picture: Mapped[str | None] = mapped_column(String(250))
    bio: Mapped[str | None] = mapped_column(String(300))
    posts: Mapped[list['Post']] = relationship(back_populates='author')
    followers: Mapped[list['Follow']] = relationship(foreign_keys='Follow.following_id', back_populates='following')
    following: Mapped[list['Follow']] = relationship(foreign_keys='Follow.follower_id', back_populates='follower')
    likes: Mapped[list['Like']] = relationship(back_populates='user')
    comments: Mapped[list['Comment']] = relationship(back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "bio": self.bio,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    author: Mapped['User'] = relationship(back_populates='posts')
    likes: Mapped[list['Like']] = relationship(back_populates='post')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "user_id": self.user_id,
        }
    
class Follow(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    follower: Mapped['User'] = relationship(foreign_keys=[follower_id], back_populates='following')
    following: Mapped['User'] = relationship(foreign_keys=[following_id], back_populates='followers')

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id,
        }
    
class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='likes')
    post: Mapped['Post'] = relationship(back_populates='likes')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }