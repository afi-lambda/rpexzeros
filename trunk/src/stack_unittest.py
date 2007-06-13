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
        def test( clk, reset, enable, push_pop, input_1, output_1, output_2 ):

            """
            def push_pop( val=0, pp=True,push_pop=push_pop, enable=enable, input_1=input_1 ):
                enable.next = 1
                input_1.next = val
                push_pop.next = pp

            def clean_flags( reset=reset, enable=enable, input_1=input_1, push_pop=push_pop ):
                reset.next = 0
                enable.next = 0
                push_pop.next = 0
                input_1.next = 0
            """
            #######################
            ## INICIO DOS TESTES ##
            #######################

            #Push test1:
            #push_pop( 110, 0 )
            enable.next = 1
            input_1.next = 110
            push_pop.next = 0
            yield clk.posedge
            yield clk.negedge
            #clean_flags()
            reset.next = 0
            enable.next = 0
            push_pop.next = 0
            input_1.next = 0
            self.assertEqual( output_1, 110 )
            self.assertEqual( output_2, 0 )

            #Push test2:
            #push_pop( 120, 0 )
            enable.next = 1
            input_1.next = 120
            push_pop.next = 0
            yield clk.posedge
            yield clk.negedge
            reset.next = 0
            enable.next = 0
            push_pop.next = 0
            input_1.next = 0
            self.assertEqual( output_1, 120 )
            self.assertEqual( output_2, 110 )

            #Pop test1:
            #push_pop(10,True)
            enable.next = 1
            input_1.next = 10
            push_pop.next = 1
            yield clk.posedge
            yield clk.negedge
            reset.next = 0
            enable.next = 0
            push_pop.next = 0
            input_1.next = 0
            self.assertEqual( output_1, 110 )
            self.assertEqual( output_2, 0 )

            #Pop test2:
            enable.next = 1
            input_1.next = 20
            push_pop.next = 1
            yield clk.posedge
            yield clk.negedge
            reset.next = 0
            enable.next = 0
            push_pop.next = 0
            input_1.next = 0
            self.assertEqual( output_1, 0 )
            self.assertEqual( output_2, 0 )

            raise StopSimulation

            """for i in range( 10 ):
                if i == 8: reset.next = 1
                enable.next = 1
                input_1.next = 100 + i
                push_pop.next = 0
                yield clk.posedge

                if i != 9:
                    self.assertEqual( output_1, 100 )
                else:
                    self.assertEqual( output_1, 0 )
                if i == 0 or i == 9: self.assertEqual( output_2, 0 )
                elif i == 1: self.assertEqual( output_2, 100 )
            raise StopSimulation
            """

        clk_s = Signal( bool( 1 ) )
        reset_s, enable_s = [Signal( bool( 0 ) ) for i in range( 2 )]
        push_pop_s = Signal( 1 )
        output_1_s, output_2_s = [Signal( 0 ) for i in range( 2 )]
        input_1_s = Signal( intbv( 0 )[32:] )

        clkgen = clk_gen( clk_s )
        check = test( clk_s, reset_s, enable_s, push_pop_s, input_1_s, output_1_s, output_2_s )
        device = stack( clk_s, reset_s, enable_s, push_pop_s, input_1_s, output_1_s, output_2_s )

        sim = Simulation( clkgen, device, check )
        sim.run( quiet=1 )

if __name__ == '__main__':
    unittest.main()

