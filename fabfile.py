from datetime import date

import git
from fabric.api import lcd, local

from fabenv import version_file
from progstrat.installed_apps import installed_apps


def update_change_log(version, new):
    try:
        g = git.Git('./')
        log = g.log('%s..' % version, '--no-merges', '--pretty=format:%s').split('\n')
        today = date.today()
        with open('CHANGELOG.md', 'r') as old_changelog:
            old = old_changelog.read()
        minus_header = "\n".join(old.split('\n')[1:])
        with open('CHANGELOG.md', 'w') as new_changelog:
            new_changelog.write('#CHANGELOG\n\n')
            new_changelog.write('##Version %s (%s)\n\n' % (new, today))
            for line in log:
                new_changelog.write("* " + line + "\n")
            new_changelog.write('\n')
            new_changelog.write(minus_header)
    except Exception as ex:
        print ex


def bump_patch():
    with open(version_file, 'r') as f:
        original = f.read()
        version = original.split('=')[1].strip('\" \n\'')
        major, minor, patch = version.split('.')
        patch = int(patch) + 1
        new_version = '%s.%s.%s' % (major, minor, patch)
    update_change_log(version, new_version)
    with open(version_file, 'w') as f:
        f.write('__version__ = "%s.%s.%s"' % (major, minor, patch))
    local('git add %s' % version_file)
    local('git add CHANGELOG.md')
    local('git commit -m "updated version to %s.%s.%s"' % (major, minor, patch))
    local('git tag %s.%s.%s -m "Update for release"' % (major, minor, patch))


def bump_minor():
    with open(version_file, 'r') as f:
        original = f.read()
        version = original.split('=')[1].strip('\" \n\'')
        major, minor, patch = version.split('.')
        patch = 0
        minor = int(minor) + 1
        new_version = '%s.%s.%s' % (major, minor, patch)
    update_change_log(version, new_version)
    with open(version_file, 'w') as f:
        f.write('__version__ = "%s.%s.%s"' % (major, minor, patch))
    local('git add %s' % version_file)
    local('git add CHANGELOG.md')
    local('git commit -m "updated version to %s.%s.%s"' % (major, minor, patch))
    local('git tag %s.%s.%s -m "Update for release"' % (major, minor, patch))


def bump_major():
    with open(version_file, 'r') as f:
        original = f.read()
        version = original.split('=')[1].strip('\" \n\'')
        major, minor, patch = version.split('.')
        patch = 0
        minor = 0
        major = int(major) + 1
        new_version = '%s.%s.%s' % (major, minor, patch)
    update_change_log(version, new_version)
    with open(version_file, 'w') as f:
        f.write('__version__ = "%s.%s.%s"' % (major, minor, patch))
    local('git add %s' % version_file)
    local('git add CHANGELOG.md')
    local('git commit -m "updated version to %s.%s.%s"' % (major, minor, patch))
    local('git tag %s.%s.%s -m "Update for release"' % (major, minor, patch))


def cut(release='patch'):
    test()
    if release == 'patch':
        bump_patch()
    elif release == 'minor':
        bump_minor()
    elif release == 'major':
        bump_major()
    elif release == 'none':
        pass
    local('git push --follow-tags')


def vagrant(subcommand):
    with lcd('vagrant'):
        local('vagrant {}'.format(subcommand))


def freeze():
    local('pip freeze > requirements.txt')


def quality_check():
    local('pep8 .')
    local('jshint assets')
    local('xenon . -a A -m A -i core')


def test():
    app_list = " ".join(installed_apps)
    local('coverage run manage.py test %s' % app_list)
    local('coverage report --fail-under=100')
    quality_check()


def fixturize(app="All"):
    """
    Saves Fixtures to their respective files
    :return:
    """

    if app == "All":
        local('python manage.py dumpdata resources > resources/fixtures/resources.json')
        local('python manage.py dumpdata military > military/fixtures/military.json')
        local('python manage.py dumpdata arenas > arenas/fixtures/arena.json')
        local('python manage.py dumpdata sciences > sciences/fixtures/technologies.json')
        local('python manage.py dumpdata auth.Group > fixtures/groups.json')
    elif app == "resource":
        local('python manage.py dumpdata resources > resources/fixtures/resources.json')
    elif app == "military":
        local('python manage.py dumpdata military > military/fixtures/military.json')
    elif app == "arena":
        local('python manage.py dumpdata arenas > arenas/fixtures/arena.json')
    elif app == "sciences":
        local('python manage.py dumpdata sciences > sciences/fixtures/technologies.json')
    elif app == "groups":
        local('python manage.py dumpdata auth.Group > fixtures/groups.json')
