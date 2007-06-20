#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------
# Module stack
# Author: Rodrigo Peixoto
#--------------------------

from mux2 import *
from myhdl import *
from registrador import *

def stack( clk, reset, enable, push_pop_stack, input_stack_1, output_stack_1, output_stack_2 ):

    reg_1_out, reg_2_out, reg_3_out = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
    mux_1_out, mux_2_out, mux_3_out = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]

    reg_1_out = output_stack_1
    reg_2_out = output_stack_2

    inside_clear = Signal( bool( 0 ) )
    pp = push_pop_stack

    mux_1 = mux2( a=input_stack_1,
                  b=reg_2_out,
                  sel=pp,
                  result=mux_1_out )

    reg_1 = registrador( clk=clk,
                         input_1=mux_1_out,
                         enable=enable,
                         clear=inside_clear,
                         output_1=reg_1_out )

    mux_2 = mux2( a=reg_1_out,
                  b=reg_3_out,
                  sel=pp,
                  result=mux_2_out )

    reg_2 = registrador( clk=clk,
                         input_1=mux_2_out,
                         enable=enable,
                         clear=inside_clear,
                         output_1=reg_2_out )

    mux_3 = mux2( a=reg_2_out,
                  b=0,
                  sel=pp,
                  result=mux_3_out )

    reg_3 = registrador( clk=clk,
                         input_1=mux_3_out,
                         enable=enable,
                         clear=inside_clear,
                         output_1=reg_3_out )


    @always( clk.posedge )
    def process1():
        if reset:
            inside_clear.next = 1
        else:
            inside_clear.next = 0

    return process1, mux_1, reg_1, mux_2, reg_2, mux_3, reg_3

if __name__ == '__main__':
    clk, reset, enable, push_pop = [Signal( bool( 0 ) ) for i in range( 4 )]
    input_1, output_1, output_2 = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
    toVerilog( stack, clk, reset, enable, push_pop, input_1, output_1, output_2 )
