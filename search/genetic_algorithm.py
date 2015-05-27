import random
import heapq


class Gene:
    def __init__(self, value):
        self.value = value # must be a string
        self.h_score = None
    def __repr__(self, ):
        return u"%s, [score: %d]" % (self.value, self.h_score)
    


def heuristic( gene ):
    if not gene.h_score:
        gene.h_score = int(gene.value) # lower is better
    return gene.h_score
        

class GeneticSearch:
    def __init__(self, population ):
        self.population = population
        
    def _choose_parents(self, population, n_parents=2 ):
        # [ (prob, element) ]
        parents = []
        tot = sum(fitness for fitness,gene in population)
        for i in xrange(n_parents):
            chosen = random.uniform(0,tot)
            for weight,gene in population:
                chosen -= weight
                if chosen<=0:
                    parents.append(gene)
                    break
        return parents
    
    def set_fitness(self, population ):
        high, low = len(population),1
        weighted_population = [] # (weight, object) less is better. used for sorting
        
        for gene in population:
            heapq.heappush(weighted_population, (heuristic(gene),gene) )
        
        # Use Ranking
        for index,rated_gene in enumerate(weighted_population):
            rank = high-(high-low)*(float(index)/len(weighted_population))
            fitness, gene = rated_gene
            weighted_population[index] = ( rank, gene )
        
        return weighted_population

    def mutate_population(self, population ):
        for index,gene in enumerate(population):
            if random.randint( 1,20 ) == 1:
                rand1 = random.randint(0,len(gene.value)-1)
                mutate_string = list( gene.value )
                mutate_string[rand1] = str(random.randint(0,9))
                population[index] = Gene( ''.join(mutate_string) )
                
        return population

    def lamarackian_evolution(self, gene, population, generations=3, n_successors=4):
        evolved_pool = [(1,gene)] # we need to store the probabilities
        
        for _ in xrange(generations):
            new_pool = []
            for _, specialized_gene in evolved_pool:
                for _ in xrange( n_successors/2 ):
                    parents = self._choose_parents(population,n_parents=1) + [specialized_gene]
                    new_pool.extend(self.crossover( parents ))
            evolved_pool = self.set_fitness(new_pool[:n_successors])
        
        fitness, best_candidate = evolved_pool[0]
        return fitness, best_candidate
            
            
    def crossover(self, parents):
        gene1, gene2 = parents.pop().value,parents.pop().value
        pivot = random.randint(0,min(len(gene1),len(gene2))-1)+1
        return [ Gene(gene1[:pivot]+gene2[pivot:]), Gene(gene2[:pivot]+gene1[pivot:]) ]
        
    
    def breed(self, population ):
        new_population = []
        
        """ Lamarackian evolution : high time complexity, fewer generations"""
        #population = [ self.lamarackian_evolution(gene,population) for fitness, gene in population]
        
        """ Elitism """
        new_population = [gene for fitness, gene in population[:3]]
        
        n_children = (len(population) - len(new_population))/2
        for _ in xrange(0,n_children):
            new_population.extend( self.crossover(self._choose_parents(population)) )
        return self.mutate_population( new_population )
        
    def run(self ):
        g = 0
        
        weighted_population = self.set_fitness( self.population )
        current_best = heuristic( weighted_population[0][1] )
        
        while current_best!=0:
            g += 1
            self.population = self.breed( weighted_population )
            weighted_population = self.set_fitness( self.population )
            
            current_best = heuristic( weighted_population[0][1] )
            if g%100 == 0:
                print weighted_population[0][1].value, 'generations:', g
        
        print 'Solved in #generations:', g


GeneticSearch([Gene( str(random.randint(0,99999999999999999)) ) for _ in xrange(30)]).run()
