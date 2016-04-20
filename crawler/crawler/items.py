from scrapy.item import Item, Field

class VacationItem(Item):
    url = Field()
    createdAt = Field()
    term = Field()
    locationFrom = Field()
    food = Field()
    days = Field()
    price = Field()
    urlCrawled = Field()
