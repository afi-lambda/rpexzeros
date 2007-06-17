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
    def test_case_push_pop( self ):
        """Pushes seguidos de pops"""
        def test( clk, reset, enable, push_pop, input_1, output_1, output_2 ):


            def push_pop_method( val=0, pp=True, push_pop=push_pop, enable=enable, input_1=input_1 ):
                enable.next = 1
                input_1.next = val
                push_pop.next = pp


            def clean_flags_method( reset=reset, enable=enable, input_1=input_1, push_pop=push_pop ):
                reset.next = 0
                enable.next = 0
                push_pop.next = 0
                input_1.next = 0

            #######################
            ## INICIO DOS TESTES ##
            #######################

            #Push test1:
            push_pop_method( 110, 0 )
            yield clk.posedge
            yield clk.negedge
            clean_flags_method()
            self.assertEqual( output_1, 110 )
            self.assertEqual( output_2, 0 )

            #Push test2:
            push_pop_method( 120, 0 )
            yield clk.posedge
            yield clk.negedge
            clean_flags_method()
            self.assertEqual( output_1, 120 )
            self.assertEqual( output_2, 110 )

            #Pop test1:
            push_pop_method( 10, True )
            yield clk.posedge
            yield clk.negedge
            clean_flags_method()
            self.assertEqual( output_1, 110 )
            self.assertEqual( output_2, 0 )

            #Pop test2:
            push_pop_method( 20, True )
            yield clk.posedge
            yield clk.negedge
            clean_flags_method()
            self.assertEqual( output_1, 0 )
            self.assertEqual( output_2, 0 )

            raise StopSimulation

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

    def test_case_push_pop2( self ):
        """1000 pushes seguidos"""
        def test( clk, reset, enable, push_pop, input_1, output_1, output_2 ):


            def push_pop_method( val=0, pp=True, push_pop=push_pop, enable=enable, input_1=input_1 ):
                enable.next = 1
                input_1.next = val
                push_pop.next = pp


            def clean_flags_method( reset=reset, enable=enable, input_1=input_1, push_pop=push_pop ):
                reset.next = 0
                enable.next = 0
                push_pop.next = 0
                input_1.next = 0

            #######################
            ## INICIO DOS TESTES ##
            #######################

            current, previous = 0, 0

            for i in range( 1000 ):
                previous = current
                current = randrange( 500 )
                push_pop_method( current, 0 )
                yield clk.posedge
                yield clk.negedge
                clean_flags_method()
                self.assertEqual( output_1, current )
                self.assertEqual( output_2, previous )

            raise StopSimulation

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

