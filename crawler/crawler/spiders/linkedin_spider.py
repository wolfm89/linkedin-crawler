#!/usr/bin/python
import scrapy

class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    start_urls = [
        'https://www.linkedin.com/'
    ]

    def parse(self, response):
        login_form = response.css('.login-form').extract_first()
        return scrapy.FormRequest.from_response(
            response,
            formdata = {'session_key': 'test.test@test.com',
                        'session_password': '123456'},
            callback = self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if b'login-error' in response.body:
            self.logger.error("Login failed")
            return
        else:
            self.logger.info("Login successful")
