# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

from biosim.island import Island


def test_initiate_island():
    I = Island("OOO\nOJO\nOOO")
    assert isinstance(I, Island)