from email.policy import default
from utils.db_api.db_gino import TimedBaseModel


from sqlalchemy import Column, BigInteger,ForeignKey, String, sql

class Words(TimedBaseModel):
    __tablename__ = 'words'
    id = Column(BigInteger, primary_key=True)
    dict_id = Column(BigInteger, ForeignKey('dictionaries.id',  ondelete='CASCADE'))
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'))
    dictname = Column(String(200))
    word_ru = Column(String(200))
    word_en = Column(String(200))
    attempt = Column(BigInteger,  default=0)
    successful_attempt = Column(BigInteger, default=0)

    query : sql.select