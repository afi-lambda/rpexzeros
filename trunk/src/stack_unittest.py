#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------
# Module stack_unittest
# Author: Rodrigo Peixoto
#--------------------------

from exceptions  import Exception
from myhdl import Signal, intbv, always, delay, instance, Simulation, StopSimulation
from random import randrange
from stack import *
from utils.clock_generator import *
import unittest

STACK_LEN = 3
VIEW_STATUS = False
class stack_unittest( unittest.TestCase ):

    def test_case_push_pop( self ):
        """Pushes seguidos de pops 1000 vezes"""
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

            def print_status( flag=VIEW_STATUS, output_1=output_1, output_2=output_2 ):
                if flag:
                    print output_1
                    print output_2

            #######################
            ## INICIO DOS TESTES ##
            #######################
            for test in range( 1000 ):
                fake_stack = []
                for i in range( STACK_LEN ):
                    #Randomic generation numbers
                    randomic_number = randrange( 200 )
                    previous_randomic_number = 0
                    if fake_stack: # != []
                        previous_randomic_number = fake_stack[-1]

                    #Push fake stack
                    fake_stack.append( randomic_number )

                    #Push in the actual stack
                    push_pop_method( randomic_number, 0 )
                    yield clk.posedge
                    yield clk.negedge
                    clean_flags_method()
                    print_status()

                    #Verify the transaction
                    self.assertEqual( output_1, randomic_number )
                    self.assertEqual( output_2, previous_randomic_number )

                for i in range( STACK_LEN ):
                    #Pop stack
                    fake_stack.pop()
                    current_stack_top = 0
                    next_stack_top = 0
                    if fake_stack: current_stack_top = fake_stack[-1]
                    if len( fake_stack ) > 1: next_stack_top = fake_stack[-2]

                    #Pop actual stack
                    push_pop_method( 10, True )
                    yield clk.posedge
                    yield clk.negedge
                    clean_flags_method()
                    print_status()

                    #Verify the transaction
                    self.assertEqual( output_1, current_stack_top )
                    self.assertEqual( output_2, next_stack_top )

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

