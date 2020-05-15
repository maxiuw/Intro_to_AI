a = set()
a.add(4)
a.add(5)

b = set()
b.add(3)
b.add(4)

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96,
        'name':'Maciek'
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        },
        'name':"tat"
    },

    # Mutation probability
    "mutation": {
        'm':0.01,
        'name':'krysia'
    }
}

names = ['gene','trait','annna']

for i in PROBS:
    print(PROBS[i]['name'])
    print(i in names)
k = dict()
# k={'C':{True: 0,False: 0}}
# k['C'][True] = 3
k['c'] =3