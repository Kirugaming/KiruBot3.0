from datetime import datetime

from discord.ext.commands import Context
from sqlalchemy import create_engine, Column, Integer, String, DateTime, PickleType
from sqlalchemy.orm import declarative_base, sessionmaker

# Create database engine and create a base class which will be used to create the table
database_engine = create_engine('sqlite:///db.sqlite3', echo=False, future=True)
Session = sessionmaker(bind=database_engine)
Base = declarative_base()


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, nullable=False)
    creator_id = Column(String, nullable=False)
    creator_name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date_made = Column(DateTime, default=datetime.utcnow)
    alert_date = Column(DateTime, nullable=False)
    channel_id_to_announce = Column(Integer, nullable=False)
    role_to_announce = Column(String, nullable=False)

    def __repr__(self):
        return f"<Schedule(guild_id={self.guild_id}, creator_id={self.creator_id}, creator_name={self.creator_name}, content={self.content}, date_made={self.date_made}, alert_date={self.alert_date}, channel_id_to_announce={self.channel_id_to_announce}, role_to_announce={self.role_to_announce})"


class RoleSelectionView(Base):
    __tablename__ = "role_selection_view"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, nullable=False)
    selected_roles = Column(PickleType, nullable=False)

    def __repr__(self):
        return f"<RoleSelectionView(channel_id={self.channel_id}, selected_roles={self.selected_roles})"


def create_tables():
    Base.metadata.create_all(database_engine)

