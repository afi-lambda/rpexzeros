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
import os
from myhdl import *

memory_data = []

def fetch_system_memory():
    mem = []
    try:
        file = open( "/tmp/rpexz_memory.tmp", 'r' )
        mem = file.readlines()
        filter = lambda a: int( a[:-1] )
        mem = map( filter, mem )
        file.close()
    except IOError:
        pass
    return mem

def memory( enable, reset, address, read_write, data_in, data_out ):
    """This is the rpexz memory module.
    enable - (1 bit input): enable the memory use
    reset - (1 bit input): memory's reset
    address - (8 bits input): the read_write memory address
    read_write - (1 bit input): 0 read; 1 write
    data_in - (32 bits input): memory input data
    data_out - (32 bist output): memory output data
    """
    @always( reset.posedge )
    def process1():
        try:
            memory_data = []
            os.remove( "/tmp/rpexz_memory.tmp" )
        except:
            pass

    @instance
    def process2( enable, address, read_write, data_in, data_out ):
        if enable:
            #write
            if read_write:
                memory_data[address] = data_in
            #read
            else:
                data_out.next = memory_data[address]
            yield delay( 3 )
        else:
            pass

    return process1 , process2

if __name__ == '__main__':
    print fetch_system_memory()