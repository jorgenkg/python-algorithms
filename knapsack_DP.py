# -*- coding: utf-8 -*-

objects = [
    #(cost,weight,object)
    (1,4,[None]),
    (4,5,[None]),
    (3,8,[None]),
    (7,3,[None]),
    (4,30,[None]),
    (2,1,[None]),
    (8,8,[None]),
    (12,2,[None]),
]

def DP_KP( S, limit=200 ):
    TRIPLE = [(0,0,[]),S[0]]
    for i in range(1,len(S)):
        new = {}
        for k, w, SET in TRIPLE:
            weight =  w + S[i][1]
            if weight <= limit:
                cost = k + S[i][0]
                if cost in new.keys() and weight >= new[cost]: pass
                else: new[cost] = ( cost, weight, SET + S[i][2])
        TRIPLE.extend(new.values())
    return TRIPLE

print DP_KP( objects, 56 )[-1] # highest value for weight limit