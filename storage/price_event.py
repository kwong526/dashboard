from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class PriceEvent(Base):
    """ Price Event """

    __tablename__ = "price_event"

    id = Column(Integer, primary_key=True)
    traceId = Column(String(250), nullable=False)
    stockTicker = Column(String(250), nullable=False)
    timespanUnit = Column(String(250), nullable=False)
    timespanLen = Column(String(100), nullable=False)
    dateStartMonth = Column(Integer, nullable=False)
    dateStartDay = Column(Integer, nullable=False)
    dateSort = Column(String(10), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, traceId, stockTicker, timespanUnit, timespanLen, dateStartMonth, dateStartDay, dateSort):
        """ Initializes a Pricing Event """
        self.traceId = traceId
        self.stockTicker = stockTicker
        self.timespanUnit = timespanUnit
        self.timespanLen = timespanLen
        self.dateStartMonth = dateStartMonth
        self.dateStartDay = dateStartDay
        self.dateSort = dateSort
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a pricing event """
        dict = {}
        dict['id'] = self.id
        dict['traceId'] = self.traceId
        dict['stockTicker'] = self.stockTicker
        dict['timespanUnit'] = self.timespanUnit
        dict['timespanLen'] = self.timespanLen
        dict['dateStartMonth'] = self.dateStartMonth
        dict['dateStartDay'] = self.dateStartDay
        dict['dateSort'] = self.dateSort
        dict['date_created'] = self.date_created

        return dict
