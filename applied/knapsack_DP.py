# -*- coding: utf-8 -*-

objects = [
    #(cost,weight,object)
    (1,4, ["a"]),
    (4,5, ["b"]),
    (3,8, ["c"]),
    (7,3, ["d"]),
    (4,30,["e"]),
    (2,1, ["f"]),
    (8,8, ["g"]),
    (12,2,["h"]),
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

print DP_KP( objects, 24 )[-1] # highest value for weight limit