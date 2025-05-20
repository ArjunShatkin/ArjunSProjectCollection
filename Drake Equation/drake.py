from drv_START import DRV

def main():

    # the assignment suggests this distribution should range from 1.5 to 3
    R_star = DRV(dist=None, type='uniform', min=1.5, max=3.0, bins=10)


    '''Fraction of stars with planets: The assignment suggests a number approaching one here.
    I will create a simple discrete distribution to reflect this
    '''
    fp = DRV(values=[0.8,0.9,1],probabilities=[0.25,0.25,0.5])

    # the assignment suggests this distribution to range from 1-5.
    life_support = DRV(dist=None, type='normal', mean=3.0, stdev=1.0, bins=8)

    '''NASA has identified about 30 planets that have prime conditions to support life. Of these planets only,
    Earth has been proven to have life, so I am setting the mean probability at 1/30'''
    f_one = DRV(dist=None,type='normal',mean=(1/30),stdev=(1/90))

    '''Fraction intelligent: We will use as a sample for this probability. Earth has had about 100 animal 
    classes in its history. Of these classes, I have identified 4 intelligent categories: Primates, Cetacea,
    Elephants, and Cephalopods(Octopuses). Thus, the mean will be 4/100.
    Although this may seem like a conservative estimate it is important to note that I am calculating based
    on animal classes, not species. If I had created this metric based on the 1 billion historical
    species on earth, the probabilities would have dropped drammatically'''
    f_intelligent = DRV(dist=None,type='normal',mean=0.04,stdev=0.01)

    '''Fraction technologically capable: Again we will use earth as a case study. We have had one
    species that has attained technological capabilities'''
    f_tech = DRV(dist=None, type='normal', mean=0.01, stdev=0.003)

    '''L: I personally believe that humankind will exist for the long and forseeable future, based
    on our strong technological capabilites which can theoretically help us adjust to almost any crisis
    in the long term.
    I will create a discrete range with probabilities from 1 million years to 1 billion years.
    '''
    L = DRV(values = [1000000,100000000,200000000,300000000,400000000,500000000,600000000,700000000,
                      800000000,900000000,1000000000],
            probabilities=[0.05,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.05])
    N = R_star * fp * life_support * f_one * f_tech * f_intelligent * L
    N.plot(show_cumulative=True,yscale=True,title='PMF for N in the Drake Equation (Log Scaled Y)')
    expected_value = N.E()
    print(f'I estimate that the universe has {int(expected_value)} planets that we can potentially communicate with!')


main()