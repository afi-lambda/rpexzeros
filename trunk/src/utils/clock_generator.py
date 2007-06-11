#!/usr/bin/python
# -*- coding: latin-1 -*-
#-------------------------
# Module clock_generator
#-------------------------
# Author: Rodrigo Peixoto
# Date: Jun 11 2007
#------------------------------------------------
# Description: This is the clock generator unit
# of the rpexz processor.
#------------------------------------------------

from myhdl import *

CLOCK_DURATION = 10

def clk_gen( clk ):
    """Clock generator module.
    clk - ( 1 bit, out): clock signal
    """
    @always( delay (CLOCK_DURATION) )
    def process():
        clk.next = not clk
    return process