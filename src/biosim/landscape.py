# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

import textwrap
from biosim.animals import Herb
import math as m
import random


class Nature:
    def __init__(self):
        self.fodder = 0
        self.habitable = True
        self.herb_list = []
        self.carn_list = []
        self.herb_move_to_list = []
        self.herb_move_from_list = []
        self.carn_move_to_list = []
        self.carn_move_from_list = []


    def feed_all_animals(self):
        self.herb_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.herb_list:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)
            else:
                break
        self.carn_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.carn_list:
            animal.feeding(self.herb_list)


    def birth_all_animals(self):
        num_herb = len(self.herb_list)
        if num_herb >= 2:
            newborn_list = []
            for animal in self.herb_list:
                newborn = animal.will_birth(self.num_herb)
                if newborn:
                    newborn_list.append(newborn)
            for newborn in newborn_list:
                self.herb_list.append(newborn)
        num_carn = len(self.carn_list)
        if num_carn >= 2:
            newborn_list = []
            for animal in self.carn_list:
                newborn = animal.will_birth(self.num_carn)
                if newborn:
                    newborn_list.append(newborn)
            for newborn in newborn_list:
                self.carn_list.append(newborn)

    def migrate_all_animals(self, neighbors):
        for animal in self.herb_list:
            if animal.migrate():
                north_nature_square = neighbors[0]
                east_nature_square = neighbors[1]
                south_nature_square = neighbors[2]
                west_nature_square = neighbors[3]
                north_relative_abundance = (north_nature_square.fodder)/((len(north_nature_square.herb_list)+1)*animal.F)
                east_relative_abundance =  (east_nature_square.fodder)/((len(east_nature_square.herb_list)+1)*animal.F)
                south_relative_abundance = (south_nature_square.fodder)/((len(south_nature_square.herb_list)+1)*animal.F)
                west_relative_abundance = (west_nature_square.fodder)/((len(west_nature_square.herb_list)+1)*animal.F)
                if north_nature_square.habitable:
                    north_propensity = m.exp(animal._lambda*north_relative_abundance)
                else:
                    north_propensity = 0
                if east_nature_square.habitable:
                    east_propensity = m.exp(animal._lambda*east_relative_abundance)
                else:
                    east_propensity = 0
                if south_nature_square.habitable:
                    south_propensity = m.exp(animal._lambda*south_relative_abundance)
                else:
                    south_propensity = 0
                if west_nature_square.habitable:
                    west_propensity = m.exp(animal._lambda*west_relative_abundance)
                else:
                    west_propensity = 0
                total_propensity = (north_propensity+east_propensity+south_propensity+west_propensity)
                north_move_prob = north_propensity/total_propensity
                east_move_prob = north_move_prob + east_propensity/total_propensity
                south_move_prob = east_move_prob + south_propensity/total_propensity
                west_move_prob = south_move_prob + west_propensity/total_propensity
                number = random.uniform(0, 1)
                if number < north_move_prob:
                    north_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)
                elif number < east_move_prob:
                    east_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)
                elif number < south_move_prob:
                    south_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)
                elif number < west_move_prob:
                    west_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)

        for animal in self.carn_list:
            if animal.migrate():
                north_nature_square = neighbors[0]
                east_nature_square = neighbors[1]
                south_nature_square = neighbors[2]
                west_nature_square = neighbors[3]
                north_herb_weight = sum([herb.weight for herb in north_nature_square.herb_list])
                east_herb_weight = sum([herb.weight for herb in east_nature_square.herb_list])
                south_herb_weight = sum([herb.weight for herb in south_nature_square.herb_list])
                west_herb_weight = sum([herb.weight for herb in west_nature_square.herb_list])

                north_relative_abundance = (north_herb_weight) / (
                            (len(north_nature_square.carn_list) + 1) * animal.F)
                east_relative_abundance = (east_herb_weight) / (
                            (len(east_nature_square.carn_list) + 1) * animal.F)
                south_relative_abundance = (south_herb_weight) / (
                            (len(south_nature_square.carn_list) + 1) * animal.F)
                west_relative_abundance = (west_herb_weight) / (
                            (len(west_nature_square.carn_list) + 1) * animal.F)
                if north_nature_square.habitable:
                    north_propensity = m.exp(animal._lambda * north_relative_abundance)
                else:
                    north_propensity = 0
                if east_nature_square.habitable:
                    east_propensity = m.exp(animal._lambda *east_relative_abundance)
                else:
                    east_propensity = 0
                if south_nature_square.habitable:
                    south_propensity = m.exp(animal._lambda *south_relative_abundance)
                else:
                    south_propensity = 0
                if west_nature_square.habitable:
                    west_propensity = m.exp(animal._lambda *west_relative_abundance)
                else:
                    west_propensity = 0
                total_propensity = (north_propensity + east_propensity + south_propensity + west_propensity)
                north_move_prob = north_propensity / total_propensity
                east_move_prob = north_move_prob + east_propensity / total_propensity
                south_move_prob = east_move_prob + south_propensity / total_propensity
                west_move_prob = south_move_prob + west_propensity / total_propensity
                number = random.uniform(0, 1)
                if number < north_move_prob:
                    north_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)
                elif number < east_move_prob:
                    east_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)
                elif number < south_move_prob:
                    south_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)
                elif number < west_move_prob:
                    west_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)



    def aging_all_animals(self):
        for animal in self.herb_list:
            animal.age()
            animal.fitness_update()
        for animal in self.carn_list:
            animal.age()
            animal.fitness_update()

    def fodder_update(self):
        pass

    def weightloss_all_animals(self):
        for animal in self.herb_list:
            animal.weightloss()
            animal.fitness_update()
        for animal in self.carn_list:
            animal.weightloss()
            animal.fitness_update()

    def death_all_animals(self):
        self.herb_list = [
            animal for animal in self.herb_list if not animal.death()
        ]
        self.carn_list = [
            animal for animal in self.carn_list if not animal.death()
        ]

    def herbivore_number(self):
        return len(self.herb_list)

    def carnivore_number(self):
        return len(self.carn_list)

class Ocean(Nature):
    def __init__(self):
        super().__init__()
        self.habitable = False


class Mountain(Nature):
    def __init__(self):
        super().__init__()
        self.habitable = False


class Desert(Nature):
    def __init__(self):
        super().__init__()


class Savannah(Nature):
    standard_parameters = {"f_max": 300, "alpha": 0.3}
    are_params_set = False

    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
            if isinstance(new_params[key], int) or isinstance(new_params[key], float):
                continue
            else:
                raise ValueError(f'Value needs to be int or float, got:{type(new_params[key]).__name__}')
        cls.standard_parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        for key in cls.standard_parameters:
            setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self):
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__()
        self.fodder = self.f_max

    def fodder_update(self):
        self.fodder = self.fodder + self.alpha * (self.f_max - self.fodder)




class Jungle(Nature):
    standard_parameters = {"f_max": 800}
    are_params_set = False

    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
            if isinstance(new_params[key], int) or isinstance(new_params[key], float):
                continue
            else:
                raise ValueError(f'Value needs to be int or float, got:{type(new_params[key]).__name__}')
        cls.standard_parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        for key in cls.standard_parameters:
            setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self):
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__()
        self.fodder = self.f_max

    def fodder_update(self):
        self.fodder = self.f_max


