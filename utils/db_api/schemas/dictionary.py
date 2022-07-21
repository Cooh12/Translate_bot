from datetime import datetime
from utils.db_api.db_gino import TimedBaseModel


from sqlalchemy import Column, BigInteger, String, sql, ForeignKey, DateTime

class Dictionary(TimedBaseModel):
    __tablename__ = 'dictionaries'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'))
    dictname = Column(String(200))
    quantity_try = Column(BigInteger, default=0)
    successful_try = Column(BigInteger, default=0)
    last_study =Column(DateTime(True), default=None)
    query : sql.select

    