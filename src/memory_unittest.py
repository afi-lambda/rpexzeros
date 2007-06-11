#!/usr/bin/python
# -*- coding: latin-1
#-------------------------
# Module Unittest ALU
#-------------------------
# Author: Rodrigo Peixoto
# Date: May 07 2007
#------------------------------------------------
# Description: This is the unittest of the
# rpexz processor's memory.
#------------------------------------------------

from myhdl import *
import unittest
from unittest import TestCase
from random import randrange
import memory


class Memory_UnitTest( TestCase ):

    def abstract_test_case( self ):
        def test( reset, address, read_write, data_in, data_out ):

            for i in range( 100000 ):
                reset.next = True
                yield delay( 5 )


                self.assertEqual( r_clock, clk_s )
            raise StopSimulation

        address, data_in, data_out =[Signal( intbv(0)[8:] ) for i in range(3)]
        reset, read_write = Signal( bool( 0 ) ),Signal( bool( 0 ) )

        mem_test = memory.memory(enable, reset, address, read_write, data_in, data_out )
        check = test( enable, reset, address, read_write, data_in, data_out )
        sim = Simulation( mem_test, check )
        sim.run( quiet=1 )

if __name__ == '__main__':
    unittest.main()



