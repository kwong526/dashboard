from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class BuyEvent(Base):
    """ Buy Event """

    __tablename__ = "buy_event"

    id = Column(Integer, primary_key=True)
    purchase_id = Column(String(250), nullable=False)
    traceId = Column(String(250), nullable=False)
    stockTicker = Column(String(10), nullable=False)
    sellVolume = Column(Integer, nullable=False)
    buyPrice = Column(Float(24), nullable=False)
    buyDate = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, purchase_id, traceId, stockTicker, sellVolume, buyPrice, buyDate):
        """ Initializes a buy Event """
        self.purchase_id = purchase_id
        self.traceId = traceId
        self.stockTicker = stockTicker
        self.sellVolume = sellVolume
        self.buyPrice = buyPrice
        self.buyDate = datetime.datetime.now()
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a buy Event """
        dict = {}
        dict['id'] = self.id
        dict['purchase_id'] = self.purchase_id
        dict['traceId'] = self.traceId
        dict['stockTicker'] = self.stockTicker
        dict['buyPrice'] = self.buyPrice
        dict['buyDate'] = self.buyDate
        dict['sellVolume'] = self.sellVolume
        dict['date_created'] = self.date_created

        return dict
