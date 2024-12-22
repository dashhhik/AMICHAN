from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship, backref


class Base(DeclarativeBase):
    pass


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    threads_count = Column(Integer, nullable=False, default=0)

    threads = relationship(
        "Thread",
        back_populates="board",
        cascade="all, delete-orphan"  # Добавлено каскадное удаление
    )



class BanList(Base):
    __tablename__ = "ban_list"

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    reason = Column(String, nullable=True)
    banned_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, unique=True)
    thread_id = Column(Integer, ForeignKey("thread.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("post.id"), nullable=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    nickname = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    replies_count = Column(Integer, nullable=False, default=0)

    parent = relationship("Post", remote_side=[id])
    files = relationship("File", back_populates="post")


class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True, unique=True)
    board_id = Column(Integer, ForeignKey("board.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    replies_count = Column(Integer, nullable=False, default=0)
    nickname = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)

    board = relationship("Board", back_populates="threads")
    posts = relationship(
        "Post",
        cascade="all, delete-orphan"  # Оставляем каскадное удаление
    )
    files = relationship("File", back_populates="thread")


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, unique=True)
    thread_id = Column(Integer, ForeignKey("thread.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=True)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    thread = relationship("Thread", back_populates="files")
    post = relationship("Post", back_populates="files")


class Admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    role = relationship("Role", back_populates="admins")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    permissions = Column(Text, nullable=True)

    admins = relationship("Admins", back_populates="role")
