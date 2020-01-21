# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

import pytest
from biosim.simulation import BioSim
import glob
import os
import os.path

def test_simulation_set_animal_parameters():
    """Test to see that incorrect species string gives ValueError"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    with pytest.raises(ValueError):
        sim.set_animal_parameters("Omnivore", {"w_birth": 8.0})

def test_simulation_set_landscape_parameters():
    """Test to see that incorrect landscape string gives ValueError"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    with pytest.raises(ValueError):
        sim.set_landscape_parameters("D", {"fodder": 8.0})

def test_simulation_make_movie_no_base():
    """Test to see that trying to create movies with no img_base raises
    RuntimeError"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    sim.simulate(5, 1)
    with pytest.raises(RuntimeError):
        sim.make_movie()

@pytest.fixture
def figfile_root():
    """Provide name for figfile root and delete figfiles after test completes"""

    ffroot = os.path.join(".", "data\dv")
    yield ffroot
    for f in glob.glob(ffroot + "_0*.png"):
        os.remove(f)


def test_simulation_make_movie_mp4():
    """Test to see that movie can be made with mp4 format"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1, img_base=figfile_root)
    sim.simulate(5, 1)
    sim.make_movie()