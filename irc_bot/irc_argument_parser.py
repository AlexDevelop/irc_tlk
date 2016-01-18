import os
import itertools
from datetime import datetime as dt, timedelta
import sys
sys.path.append('/home/hvhoek/alex/irc_tlk')

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
import django
django.setup()

from peewee_db import Todos_Todolist
from pytz import timezone
from todos.models import Setting, SettingData


class ArgumentParser(object):
    name = 'abstract'
    argument_leader = '!'
    argument_key = None
    args = None
    data = None
    allowed_functions = []
    nick = None

    def __init__(self, key=None, *args, **kwargs):
        if 'nick' in kwargs:
            self.nick = kwargs['nick']
        if 'channel' in kwargs:
            self.channel = kwargs['channel']

        if getattr(self, 'commands', None):
            # commands = [x.commands for x in ArgumentParser.__subclasses__() if getattr(x, 'commands', None)]
            # commands = list(itertools.chain.from_iterable(commands))
            self.allowed_functions = self.commands  # list(itertools.chain.from_iterable([commands, self.allowed_functions]))
        if key or self.name == '!help':
            self.argument_key = key
            try:
                self.args = key.split(' ')[1:]
                for k, value in enumerate(self.args):
                    self.args[k] = self.args[k].rstrip()
            except AttributeError:
                pass

            self.data = self.run()

    def get_subclasses(self):
        return [x.name for x in ArgumentParser.__subclasses__()]  # + ["{}help".format(self.argument_leader), ]

    def run(self):
        raise NotImplementedError("Please Implement this method")

    def get_commands(self):
        return self.allowed_functions


class HelpArgument(ArgumentParser):
    name = '!help'

    def run(self):
        try:
            command = self.args[0]
            plugin_class = "{}Argument".format(command.capitalize())
            plugin_class = globals()[plugin_class]
            self.data = ' -- '.join(plugin_class().get_commands())
            return self.data
        except (IndexError, TypeError):
            data_list = self.get_subclasses()
            self.data = ' -- '.join(data_list)
            return self.data


class LeaddArgument(ArgumentParser):
    data = dict()
    name = '!leadd'
    commands = ({'!lead add <NICK> <RANK>', '!lead remove <NICK>', '!lead reset', '!lead list'})

    def add(self, *args):
        name = args[0]
        rank = args[1]
        self.data[name] = rank

    def remove(self, *args):
        name = args[0]
        if name in self.data:
            self.data.pop(name)

    def reset(self, *args):
        self.data.clear()

    def list(self):
        data_list = ["Name: {} Rank: {}".format(x, self.data[x]) for x in self.data.keys()]
        if data_list:
            return ' -- '.join(data_list)
        return 'No leaders have been added yet. !lead add nick rank'

    def run(self):
        command = self.args[0]
        try:
            response = getattr(self, command)(*self.args[1:])
            return response
        except AttributeError:
            print('START DEBUG:')
            print(self.argument_key)
            print(self.args)
            print('END DEBUG:')
            pass


class SfsArgument(ArgumentParser):
    default_number = 45
    name = '!sfs'

    def number(self):
        try:
            return self.args[0]
        except IndexError:
            return self.default_number

    def statss(self):
        pass

    def run(self):
        print('SFFSFS run {}'.format(self.number()))

class SettingArgument(ArgumentParser):
    name = '!setting'
    commands = ({'!setting list', '!setting add channel !command on|off'})

    def add(self, *args):
        channel= args[0]
        _key = args[1]
        _value = args[2]
        setting_data, created = SettingData.objects.get_or_create(_key=_key)
        setting_data._value = _value
        setting_data.save()
        print(setting_data, created)
        name = "{}_{}".format(_key, _value)
        setting, created = Setting.objects.get_or_create(name=name, channel=channel, setting_data=setting_data)
        print(setting, created)

    def remove(self, *args):
        pass

    def list(self, *args):
        pass

    def run(self):
        command = self.args[0]
        try:
            response = getattr(self, command)(*self.args[1:])
            return response
        except AttributeError:
            print('START DEBUG:')



class ReminderArgument(ArgumentParser):
    name = '!reminder'
    commands = ({'!reminder <MINUTE> <TEXT>'})

    def run(self):
        try:
            minutes = int(self.args[0])
            description = " ".join(self.args[1:])
            tz_custom = timezone('Europe/Amsterdam')
            dt_future = tz_custom.localize(dt.utcnow()) + timedelta(minutes=minutes)
            todo_object = Todos_Todolist.create(data=self.channel, created=dt.utcnow(), modified=dt.utcnow(),
                                                name=self.nick, date_deadline=dt_future, todo_type_id=3,
                                                description=description, identifier=99999999, status=0)
            if todo_object:
                self.data = "Added a reminder for {user} in {min} minute(s) - date: {dt} (UTC)".format(
                        user=self.nick, min=minutes, dt=dt_future)
                return self.data
        except Exception as e:
            print(e, 'errrooorrr')

# print(ReminderArgument('!reminder 30 something').data)
# print(HelpArgument().data)
# print(HelpArgument('!help lead').data)
# print(HelpArgument('!help sfs').data)
# LeadArgument('lead add livvo leg')
# LeadArgument('lead add livvoo xxx')
# print(LeadArgument('lead list').data)
