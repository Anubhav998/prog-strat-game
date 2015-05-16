"""
This file is a prebuilt library to wrap splinter. It goes with the environments.py
You can use it to quickly setup tests using only feature files. For more splinter documentation
visit their site at http://splinter.cobrateam.info/
The browser object you would use in splinter is available via context.browser

It is lovingly shared and free to use and modify by Ryan McDevitt (http://mc706.com)
"""
import time

from behave import use_step_matcher, given, when, then


use_step_matcher("re")


@given('I am on (?:the )?page with url "(?P<url>.*)"')
def step_impl(context, url):
    context.browser.visit(url)


@when('I put "(?P<value>.*)" in the field with (?P<selector>name|id|css|xpath) "(?P<key>.*)"')
def step_impl(context, value, selector, key):
    if value == "null":
        value = ""  # allows you to put "null" into a field to not fill it in
    if selector == "name":
        context.browser.fill(key, value)
    elif selector == "id":
        context.browser.find_by_id(key).fill(value)
    elif selector == "css":
        context.browser.find_by_css(key).fill(value)
    elif selector == "xpath":
        context.browser.find_by_xpath(key).fill(value)


@when(
    'I (?P<action>click|mouse\wover|right\wclick|double\wclick) the (?:button|element) with (?P<selector>name|id|css|xpath) "(?P<value>.*)"')
def step_impl(context, action, selector, value):
    if action == "click":
        if selector == 'name':
            context.browser.find_by_name(value).click()
        elif selector == 'id':
            context.browser.find_by_id(value).click()
        elif selector == 'css':
            context.browser.find_by_css(value).click()
        elif selector == "xpath":
            context.browser.find_by_xpath(value).click()
    elif action == "mouse over":
        if selector == 'name':
            context.browser.find_by_name(value).mouse_over()
        elif selector == 'id':
            context.browser.find_by_id(value).mouse_over()
        elif selector == 'css':
            context.browser.find_by_css(value).mouse_over()
        elif selector == "xpath":
            context.browser.find_by_xpath(value).mouse_over()
    elif action == "right click":
        if selector == 'name':
            context.browser.find_by_name(value).right_click()
        elif selector == 'id':
            context.browser.find_by_id(value).right_click()
        elif selector == 'css':
            context.browser.find_by_css(value).right_click()
        elif selector == "xpath":
            context.browser.find_by_xpath(value).right_click()
    elif action == "double click":
        if selector == 'name':
            context.browser.find_by_name(value).double_click()
        elif selector == 'id':
            context.browser.find_by_id(value).double_click()
        elif selector == 'css':
            context.browser.find_by_css(value).double_click()
        elif selector == "xpath":
            context.browser.find_by_xpath(value).double_click()


@when('I click the link with (?P<selector>id|text|href) "(?P<value>.*)"')
def step_impl(context, selector, value):
    if selector == "id":
        context.browser.find_by_id(value).click()
    elif selector == "text":
        context.browser.click_link_by_text(value)
    elif selector == "href":
        context.browser.click_link_by_href(value)


@when('I choose the "(?P<value>.*)" option from the radio buttons with name "(?P<key>.*)"')
def step_impl(context, value, key):
    context.browser.choose(key, value)


@when('I choose the "(?P<value>.*)" option from the dropdown with name "(?P<key>.*)"')
def step_impl(context, value, key):
    context.browser.select(key, value)


@when('I (?P<bool>check|uncheck) the checkbox with name "(?P<key>.*)"')
def step_impl(context, bool, key):
    if bool == "check":
        context.browser.check(key)
    elif bool == "uncheck":
        context.browser.uncheck(key)


@when('I wait (?P<x>\d+) second(?:s)?')
def step_impl(context, x):
    time.sleep(float(x))


@when('I (?:refresh|reload) the page')
def step_impl(context):
    context.browser.reload()


@when('I hit the (?P<direction>back|forward) button')
def step_impl(context, direction):
    if direction == "back":
        context.browser.back()
    elif direction == "forward":
        context.browser.forward()


@then('I should be on (?:the )?page with url "(?P<url>.*)"')
def step_impl(context, url):
    time.sleep(1)  # wait 1 second to make sure things resolve
    assert context.browser.url == url, "Expected to be on page %s, instead got %s" % (url, context.browser.url)


@then('I should be on page with title "(?P<title>.*)"')
def step_impl(context, title):
    assert context.browser.title == title, "Expected title to be %s, instead got %s" % (title, context.browser.title)


@then('I should (?P<not_>not )?see (?:the )?text "(?P<text>.*)"')
def step_impl(context, not_, text):
    if not_:
        assert not context.browser.is_text_present(text)
    else:
        assert context.browser.is_text_present(text)


@then('I should (?P<not_>not )?see the following text')
def step_impl(context, not_):
    if not_:
        assert not context.browser.is_text_present(context.text)
    else:
        assert context.browser.is_text_present(context.text)


@then('I should (?P<not_>not )?see an element with (?P<selector>name|id|css|xpath|tag) "(?P<value>.*)"')
def step_impl(context, not_, selector, value):
    if not_:
        if selector == "css":
            assert not context.browser.is_element_present_by_css(value)
        elif selector == "id":
            assert not context.browser.is_element_present_by_id(value)
        elif selector == "tag":
            assert not context.browser.is_element_present_by_tag(value)
        elif selector == "name":
            assert not context.browser.is_element_present_by_name(value)
        elif selector == "xpath":
            assert not context.browser.is_element_present_by_xpath(value)
    else:
        if selector == "css":
            assert context.browser.is_element_present_by_css(value)
        elif selector == "id":
            assert context.browser.is_element_present_by_id(value)
        elif selector == "tag":
            assert context.browser.is_element_present_by_tag(value)
        elif selector == "name":
            assert context.browser.is_element_present_by_name(value)
        elif selector == "xpath":
            assert context.browser.is_element_present_by_xpath(value)


@then(
    'I should see (?:an )element with (?P<selector>name|id|css|xpath) "(?P<value>.*)" that has (?P<check>text|class) "(?P<text>.*)"')
def step_impl(context, selector, value, check, text):
    if check == "text":
        if selector == 'name':
            assert context.browser.find_by_name(value).text == text
        elif selector == 'id':
            assert context.browser.find_by_id(value).text == text
        elif selector == 'css':
            assert context.browser.find_by_css(value).text == text
        elif selector == "xpath":
            assert context.browser.find_by_xpath(value).text == text
    elif check == "class":
        if selector == 'name':
            assert context.browser.find_by_name(value).has_class(text)
        elif selector == 'id':
            assert context.browser.find_by_id(value).has_class(text)
        elif selector == 'css':
            assert context.browser.find_by_css(value).has_class(text)
        elif selector == "xpath":
            assert context.browser.find_by_xpath(value).has_class(text)