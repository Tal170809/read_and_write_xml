# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:48:55 2020

@author: Administrator
"""

from lxml import objectify
import pandas as pd

E = objectify.ElementMaker(annotate=False)

def add_analog_bcu(branch, var_name, var_id, var_size, num, alt_name):  
    analog_bcu = E.analogue_variable(
            E.name(
                    E.english(var_name),
                    E.alternate_language("Alt: "+alt_name)
                    ),
            E.variable_source("NDM_VARIABLE"),
            E.id(var_id),
            E.variable_size(var_size),
            E.carId(1),
            E.unit("BCU"),
            E.bogie("BOGIE_A"),
            E.comms_values(
                    E.minimum(0),
                    E.maximum(65535)
            ),
            E.display_values(
                    E.minimum(0),
                    E.maximum(65535)
                    ),
            E.colour(
                    E.red(0),
                    E.green(0),
                    E.blue(0)
                    ),
            E.guage_id(num),
            E.variable_name(var_name)
            )
    branch.append(analog_bcu)


def add_digital_bcu(branch, var_name, var_id, var_size, num, alt_name):
    digital_bcu = E.digital_led(
            E.name(
                    E.english(var_name),
                    E.alternate_language("Alt: "+alt_name)
                    ),
            E.variable_source("NDM_VARIABLE"),
            E.id(var_id),
            E.variable_size(var_size),
            E.car_id(1),
            E.unit("BCU"),
            E.bogie("BOGIE_A"),
            E.led_id(num),
            E.clear_colour(
                    E.red(255),
                    E.green(0),
                    E.blue(0)
                    ),
            E.set_colour(
                    E.red(0),
                    E.green(255),
                    E.blue(0)
                    ),
            E.variable_name(var_name)
            )
    branch.append(digital_bcu)
    
def add_analog_physical(branch, var_name, var_id, var_size, num, alt_name):
    analog_physical = E.analogue_variable(
            E.name(
                    E.english(var_name),
                    E.alternate_language("Alt: "+alt_name)
                    ),
            E.variable_source("PHYSICAL_VARIABLE"),
            E.id(var_id),
            E.variable_size(var_size),
            E.carId(1),
            E.unit("BCU"),
            E.bogie("BOGIE_A"),
            E.comms_values(
                    E.minimum(0),
                    E.maximum(65535)
            ),
            E.display_values(
                    E.minimum(0),
                    E.maximum(65535)
                    ),
            E.colour(
                    E.red(0),
                    E.green(0),
                    E.blue(0)
                    ),
            E.guage_id(num),
            E.variable_name(var_name))
    branch.append(analog_physical)

def add_digital_physical(branch, var_name, var_id, var_size, num, alt_name):
    digital_physical = E.digital_led(
            E.name(
                    E.english(var_name),
                    E.alternate_language("Alt: "+alt_name)
                    ),
            E.variable_source("PHYSICAL_VARIABLE"),
            E.id(var_id),
            E.variable_size(var_size),
            E.car_id(1),
            E.unit("BCU"),
            E.bogie("BOGIE_A"),
            E.led_id(num),
            E.clear_colour(
                    E.red(255),
                    E.green(0),
                    E.blue(0)
                    ),
            E.set_colour(
                    E.red(0),
                    E.green(255),
                    E.blue(0)
                    ),
            E.variable_name(var_name)
            )
    branch.append(digital_physical)
            
