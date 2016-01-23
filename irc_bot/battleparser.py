soldier_types = (
    'Commanders',
    'Heroes',
    'Artillery',
    'Cavalry',
    'Infantry',
)


class BattleParserIrc(object):

    line_number_length = 7
    lines = []

    def __init__(self, data):
        self.db_object = data
        self.attacker = data['attacker']
        self.defender = data['defender']
        self.lines = []

    def check_for_number(self, data_string):
        if " " in data_string:
            return data_string.split(' ')
        if data_string.isnumeric():
            data_string = int(data_string)
        return data_string, False

    def format_to_same_length(self, data_string, length=15, reverse=False):
        _name, _number = self.check_for_number(data_string)
        if _number:
            total = length - len(_name) - len(str(_number))
        else:
            total = length - len(str(_name))

        if reverse:
            total -= 2

        if _number:
            if reverse:
                line_str = "".join([_name, "".join([" " for x in range(1, total)]), str(_number),])
            else:
                line_str = "".join([_name, str(_number), "".join([" " for x in range(1, total)])])
        else:
            if str(_name).isnumeric() and reverse:
                line_str = "".join(["".join([" " for x in range(1, total)]), str(_name), '  '])
            else:
                if reverse:
                    line_str = "".join(["".join([" " for x in range(1, total)]), str(_name), '  '])
                else:
                    line_str = "".join([str(_name), "".join([" " for x in range(1, total)]),])

        return line_str


    def get_type(self):
        irc_string = self.format_to_same_length('Soldiers', length=12)
        irc_string += self.format_to_same_length('Tot', length=self.line_number_length, reverse=True)
        irc_string += self.format_to_same_length('Inj', length=self.line_number_length, reverse=True)
        irc_string += self.format_to_same_length('Dead', length=self.line_number_length, reverse=True)
        irc_string += self.format_to_same_length('Capt', length=self.line_number_length + 2, reverse=True)

        irc_string += self.format_to_same_length('Soldiers', length=12)
        irc_string += self.format_to_same_length('Tot', length=self.line_number_length, reverse=True)
        irc_string += self.format_to_same_length('Inj', length=self.line_number_length, reverse=True)
        irc_string += self.format_to_same_length('Dead', length=self.line_number_length, reverse=True)
        irc_string += self.format_to_same_length('Capt', length=self.line_number_length, reverse=True)

        self.lines.append(irc_string)

    def get_soldiers_for_each_type(self):
        for type in soldier_types:
            irc_string = self.format_to_same_length(type, length=12)
            irc_string += self.format_to_same_length('{}'.format(self.attacker[type]['Tot']), reverse=True, length=self.line_number_length)
            irc_string += self.format_to_same_length('{}'.format(self.attacker[type]['Inj']), reverse=True, length=self.line_number_length)
            irc_string += self.format_to_same_length('{}'.format(self.attacker[type]['Dead']), reverse=True, length=self.line_number_length)
            irc_string += self.format_to_same_length('{}'.format(self.attacker[type]['Capt']), reverse=True, length=self.line_number_length + 2)

            irc_string += self.format_to_same_length(type, length=12)
            irc_string += self.format_to_same_length('{}'.format(self.defender[type]['Tot']), reverse=True, length=self.line_number_length)
            irc_string += self.format_to_same_length('{}'.format(self.defender[type]['Inj']), reverse=True, length=self.line_number_length)
            irc_string += self.format_to_same_length('{}'.format(self.defender[type]['Dead']), reverse=True, length=self.line_number_length)
            irc_string += self.format_to_same_length('{}'.format(self.defender[type]['Capt']), reverse=True, length=self.line_number_length)

            self.lines.append(irc_string)

    def run(self):
        self.format_battle_for_irc()

    def format_battle_for_irc(self):
        self.get_type()
        self.get_soldiers_for_each_type()