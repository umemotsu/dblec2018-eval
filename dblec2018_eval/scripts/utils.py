# -*- coding: utf-8 -*-


def register(group, sub_commands):
    for sc in sub_commands:
        group.add_command(sc)
