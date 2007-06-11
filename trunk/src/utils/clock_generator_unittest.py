#!/usr/bin/python

#-------------------------
# Module Unittest ALU
#-------------------------
# Author: Rodrigo Peixoto
# Date: May 07 2007
#------------------------------------------------
# Description: This is the unittest of the
# rpexz processor's Arithmetic logic unit.
#------------------------------------------------

from myhdl import *
import unittest
from unittest import TestCase
from random import randrange
import clock_generator

CLOCK_DURATION = clock_generator.CLOCK_DURATION

class Clock_generator_UnitTest( TestCase ):

    def test_case_clock_gen( self ):
        """Gerando clocks 10000 vezes"""

        def test( clk_s ):
            r_clock = Signal( bool( 0 ) )
            for i in range( 100000 ):
                yield delay( CLOCK_DURATION )
                r_clock.next = not r_clock
                self.assertEqual( r_clock, clk_s )
            raise StopSimulation


        clk = Signal( bool( 0 ) )
        clk_test = clock_generator.clk_gen( clk )
        check = test( clk )
        sim = Simulation( clk_test, check )
        sim.run( quiet=1 )


if __name__ == '__main__':
    unittest.main()
