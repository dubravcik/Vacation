import scrapy

class VacationEasy(scrapy.Spider):
    name = 'vacation_easy'
    start_urls = ["http://hotel.invia.cz/direct/tour_detail/ajax-term-select-form-terms/?formData[d_start_from]=&formData[d_end_to]=&formData[c_price_int]=-1&formData[nl_hotel_id]=52988&formData[nl_tour_id]=&nl_page=1&sortField=&sortOrder="]

    def parse(self, response):

        yield {response.url}