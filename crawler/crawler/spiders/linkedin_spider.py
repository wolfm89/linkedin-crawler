#!/usr/bin/python
import scrapy
import base64

class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    login_url = 'https://www.linkedin.com/'
    start_urls = [
        'https://www.linkedin.com/directory/people-a-33-13-13/'
    ]

    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.login)

    def login(self, response):
        with open("cred.txt") as f:
            email = base64.b64decode(f.readline())
            password = base64.b64decode(f.readline())
        return scrapy.FormRequest.from_response(
            response, formdata={'session_key': email,
                                'session_password': password},
            callback=self.check_login_response)

    def check_login_response(self, response):
        if b'login-error' in response.body:
            self.logger.error("Login failed")
            return
        else:
            self.logger.info("Login successful")
            for u in self.start_urls:
                yield scrapy.Request(u, callback=self.parse_member_dir)

    def parse_member_dir(self, response):
        self.logger.info("Got data")
