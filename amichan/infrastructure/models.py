from datetime import datetime
from functools import partial

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


relationship = partial(relationship, lazy="raise")


class Thread(Base):
    __tablename__ = "thread"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    tag_id: Mapped[int] = mapped_column(Integer, nullable=True)
    replies_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nickname: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    board_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("board.id"), nullable=False
    )

    board: Mapped["Board"] = relationship("Board", back_populates="threads")
    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="thread", lazy="raise"
    )


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thread_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("thread.id"), nullable=False
    )
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("post.id"), nullable=True
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    nickname: Mapped[str] = mapped_column(String, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    replies_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships (if needed)
    thread: Mapped["Thread"] = relationship(
        "Thread", back_populates="posts", lazy="joined"
    )
    parent: Mapped["Post"] = relationship("Post", remote_side=[id], lazy="raise")


class Board(Base):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    threads_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    threads: Mapped[list["Thread"]] = relationship("Thread", back_populates="board")
