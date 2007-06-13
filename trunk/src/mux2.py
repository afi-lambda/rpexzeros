#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------
# Module mux2
# Author: Rodrigo Peixoto
#--------------------------

from myhdl import always_comb

def mux2( a, b, sel, result ):
    """Mux de duas entradas
    a
    b
    sel
    result
    """
    @always_comb
    def process():
        if sel:
            result.next = b
        else:
            result.next = a
    return process
