import time
from urlparse import urljoin

from behave import use_step_matcher, given, then


use_step_matcher("re")


@given('I am on (?:the )?page with relative url "(?P<url>.*)"')
def step_impl(context, url):
    full_url = urljoin(context.config.server_url, url)
    context.browser.visit(full_url)


@then('I should (?P<not_>not )?be on (?:the )?page with relative url "(?P<url>.*)"')
def step_impl(context, not_, url):
    time.sleep(1)
    full_url = urljoin(context.config.server_url, url)
    if not_:
        assert not context.browser.url == full_url, "Expected not to be on page %s, instead got %s" % (
            full_url, context.browser.url)
    else:
        assert context.browser.url == full_url, "Expected to be on page %s, instead got %s" % (
            full_url, context.browser.url)


@given('a (?P<super_>super )?user with username "(?P<username>.*)" and password "(?P<password>.*)"')
def step_impl(context, super_, username, password):
    from django.contrib.auth.models import User, Group

    group, _ = Group.objects.get_or_create(name='Users')
    group.save()
    if super_:
        u = User.objects.create_superuser(username=username, email="test@test.com", password=password)
        u.save()
    else:
        u = User(username=username, email='foo@example.com')
        u.set_password(password)
        u.save()


@given('an inactive user with username "(?P<username>.*)" and password "(?P<password>.*)"')
def step_impl(context, username, password):
    from django.contrib.auth.models import User

    u = User(username=username, email='foo1@example.com')
    u.set_password(password)
    u.is_active = False
    u.save()