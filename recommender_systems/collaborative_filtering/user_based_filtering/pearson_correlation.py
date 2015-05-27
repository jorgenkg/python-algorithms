import numpy as np
import math

ratings = np.random.randint(0,6,size=(1000,10)) # users, ratings

# Calculate and update the ratings matrix based on the user's average rating
user_averages = 1.*ratings.sum(1)/(ratings != 0).sum(1)
averaged_ratings = ratings - user_averages.reshape(ratings.shape[0],-1)

lookup = {}
def sim(a, b):
    key = tuple(sorted([a,b]))
    if not key in lookup.keys():
        rated_by_a = np.where( (ratings[a,:] != 0) )[-1]
        rated_by_b = np.where( (ratings[b,:] != 0) )[-1]
        rated_by_both = np.intersect1d( rated_by_a, rated_by_b )
        
        idx = np.ones(rated_by_both.shape, dtype=int)
        a_ratings = averaged_ratings[( idx*a, rated_by_both)]
        b_ratings = averaged_ratings[( idx*b, rated_by_both)]
    
        usr1 = math.sqrt(np.dot( a_ratings.T, a_ratings ))
        usr2 = math.sqrt(np.dot( b_ratings.T, b_ratings ))
        result = np.dot( a_ratings.T, b_ratings )/(usr1*usr2)
    
        lookup[key] = result
    return lookup[key]

def neigh( a, p ):
    neighborhood = sorted( [(sim(a,x), x) for x in xrange(ratings.shape[0]) if x != a and ratings[x,p]!=0], reverse=True )
    return [n for u, n in neighborhood if u>0][:30]
    
def pred(a, p):
    avg = user_averages[a]
    neighbors = neigh(a,p)
    return avg + math.fsum(sim(a,b) * averaged_ratings[b,p] for b in neighbors) / math.fsum(sim(a,b) for b in neighbors)


"""
Test run
"""
user = 0
predicted = np.array([int(pred(user, p)+.5) for p in xrange(ratings.shape[1])]).reshape(-1,)
print "User %d's ratings:" % user, ratings[user,:]
print "Predicted for u%d:" % user, predicted
print "Prediction RMS:", math.sqrt(np.mean((ratings[user,ratings[user,:]!=0] - predicted[ratings[user,:]!=0])**2))
