
from utils.db_api.db_gino import TimedBaseModel


from sqlalchemy import Column, BigInteger, String,  sql

class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String(200),  nullable=True)
    
    query : sql.select