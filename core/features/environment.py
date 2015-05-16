"""
This file is a pre-setup environments file to make splinter play nice with behave
It is setup to take screenshots whenever of the browser if your steps fail
To change which browser you are using, change the string in Browser(). Note you may need to install Chromedriver for chrome
It is lovingly shared and free to use and modify by Ryan McDevitt (mc706.com)
"""
import datetime

import re
import os
from splinter.browser import Browser


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TODAY = datetime.date.today()
SCREENSHOT_DIRECTORY = BASE_DIR + "/screenshots/"


def before_all(context):
    context.browser = Browser('phantomjs')
    context.browser.driver.maximize_window()


def after_all(context):
    context.browser.quit()
    context.browser = None


def after_step(context, step):
    if step.status == "failed":
        day = "{0.year}_{0.month}_{0.day}".format(TODAY)
        name = '[{0}]-{1}'.format(day, step.name)
        name = re.sub(' ', '_', name)
        name = re.sub('[\\\/]', '-', name)
        name = re.sub('[\"\']', '', name)
        name += '.png'
        context.browser.driver.save_screenshot(SCREENSHOT_DIRECTORY + name)