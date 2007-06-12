#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------
# Module stack_unittest
# Author: Rodrigo Peixoto
#--------------------------

from exceptions  import Exception
from myhdl import Signal, intbv, always, delay, instance, Simulation, StopSimulation
from random import randrange
import unittest
from stack import *
from utils.clock_generator import *


class stack_unittest( unittest.TestCase ):
    def test_case_reset( self ):
        """Resetando a pilha 1000 vezes"""
        def test( clk, reset, enable, push_pop, input_1_t, output_1_t, output_2_t ):
            for i in range( 10 ):
                reset.next = 1
                yield clk.posedge
                reset.next = 0
                yield clk.posedge
                self.assertEqual( output_1_t, 0 )
                self.assertEqual( output_2_t, 0 )
            raise StopSimulation

        clk_s, reset_s, enable_s, push_pop_s = [Signal( bool( 0 ) ) for i in range( 4 )]
        output_1_s, output_2_s = [Signal( intbv( 0 )[32:] ) for i in range( 2 )]
        output_1_s.next = 1
        output_2_s.next = 1
        input_1_s = Signal( intbv( 0 )[32:] )
        clkgen = clk_gen( clk_s )
        device = stack( clk_s, reset_s, enable_s, push_pop_s, input_1_s, output_1_s, output_2_s)
        check = test(clk_s, reset_s, enable_s, push_pop_s, input_1_s, output_1_s, output_2_s)


        sim = Simulation( clkgen, device, check )
        sim.run( quiet=1 )

if __name__ == '__main__':
    unittest.main()

