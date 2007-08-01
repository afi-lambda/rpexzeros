#!/usr/bin/python
# -*- coding: latin-1 -*-
#-------------------------
# Module memory
#-------------------------
# Author: Rodrigo Peixoto
# Date: May 07 2007
#---------------------------------------------------------
# Description: This is the memory of the rpexz processor |
#---------------------------------------------------------

from myhdl import *
import os

MEMORY_DATA = {}

#def get_memory_data( address ):
#    return MEMORY_DATA[address]

#def set_memory_data( address, data ):
#    if address and data:
#        MEMORY_DATA[address] = data

def fetch_system_memory():
    mem = {}
    try:
        file = open( "/tmp/rpexz_memory.tmp", 'r' )
        mem = file.readlines()
        mem = map( str.strip, mem )
        mem = dict( enumerate( [int( x, 16 ) for x in mem] ) )
        file.close()
    except IOError:
        pass
    return mem

def memory( clk, chip_select, address, load_store, data_in, data_out ):
    """This is the rpexz memory module.
        :Signals:
            chip_select - (1 bit input): chip_select the memory use
            reset - (1 bit input): memory's reset
            address - (8 bits input): the read_write memory address
            load_store - (1 bit input): 0 read; 1 write
            data_in - (32 bits input): memory input data
            data_out - (32 bist output): memory output data
    """
    MEMORY_DATA = fetch_system_memory()

    @always( clk.posedge )
    def process2():#( chip_select, address, read_write, data_in, data_out ):

        if chip_select:
            #store
            if load_store:
                MEMORY_DATA[int( address )] = data_in
            #load
            else:
                data_out.next = MEMORY_DATA[int( address )]



    return process2

if __name__ == '__main__':
    print fetch_system_memory()