import csv
import itertools
import sys
from time import sleep
import copy
PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
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
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        # bool type
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence: # if fails_evidence != false, back to beg of the loop
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint = 1
    # print(f"ludzie ,gene {one_gene}, 2 ge {two_genes},,have t {have_trait}")
    probability = {
        person: {
            True: 0, # trait
            False: 0,
            'pass': 0, # probability of passing the 'bad' gene
            'p': 0, # probability of having particular prop (e.g. 2 genes and have trait)
            'gene': 0, # probability of getting having particular gene combination
            'type': 0
        }
        for person in people
    }
    # print(probability)
    # time.sleep(5)
    # looping in people
    for person in people:
        name = person
        # if person is a parent, just checking for parents first
        if people[person]['mother'] is None and people[person]['father'] is None:

            # two genes
            if name in two_genes:
                # analogically for all true - 2 g and have trait
                probability[name][True] = PROBS['gene'][2] * PROBS['trait'][2][True]
                # false - 2 genes and dont have trait
                probability[name][False] = PROBS['gene'][2]*PROBS['trait'][2][False]
                probability[name]['pass'] = 1 - PROBS['mutation']
                probability[name]['type'] = 2

            #one gene
            elif name in one_gene:
                probability[name][True] = PROBS['gene'][1]*PROBS['trait'][1][True]
                probability[name][False] = PROBS['gene'][1]*PROBS['trait'][1][False]
                probability[name]['pass'] = 0.5
                probability[name]['type'] = 1

            # gene 0
            else:
                probability[name][True] = PROBS['gene'][0]*PROBS['trait'][0][True]
                probability[name][False] = PROBS['gene'][0]*PROBS['trait'][0][False]
                probability[name]['pass'] = PROBS['mutation']
                probability[name]['type'] = 0


            if name in have_trait:
                probability[name]['p'] = probability[name][True]
            else:
                probability[name]['p'] = probability[name][False]
            # print(f"{name} prob {probability[name]['p']} in type {probability[name]['type'] } ")
            # sleep(1)
    #

    # children
    for child in people:
        child_name = child
        # ma rodzicow
        if people[child]['mother'] is None and people[child]['father'] is None:
            continue
        else:
            mama = people[child]['mother']
            papa = people[child]['father']

            # prob it got 2 genes from parents
            if child_name in two_genes:
                probability[child_name]['gene'] = probability[mama]['pass'] * probability[papa]['pass']
                probability[child_name]['type'] = 2
            # prob it got 1 gene from parents
            elif child_name in one_gene:
                probability[child_name]['gene'] = probability[mama]['pass']*(1-probability[papa]['pass'])\
                                                  +(probability[papa]['pass'])*(1-probability[mama]['pass'])
                probability[child_name]['type'] = 1
            # prob it got 0 genes from parents
            else:
                probability[child_name]['gene'] = (1-probability[mama]['pass'])*(1 - probability[papa]['pass'])
                probability[child_name]['type'] = 0

        # prob if it has the gene
        if child_name in have_trait:
            probability[child_name]['p'] = probability[child_name]['gene']*PROBS['trait'][probability[child_name]['type']][True]
        else:
            probability[child_name]['p'] = probability[child_name]['gene']*PROBS['trait'][probability[child_name]['type']][False]


    # multiplying all the probabilities to achieve joint
    for person in people:
        joint=joint*probability[person]['p']

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "ptrait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            probabilities[person]['gene'][2] += p
        elif person in one_gene:
            probabilities[person]['gene'][1] += p
        else:
            probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p






def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # scaling probabilities by alpha
    for person in probabilities:
        alpha1 = 1/(probabilities[person]['gene'][2]+probabilities[person]['gene'][1]+probabilities[person]['gene'][0])
        alpha2 = 1/(probabilities[person]['trait'][False]+probabilities[person]['trait'][True])
        probabilities[person]['gene'][2] = alpha1 * probabilities[person]['gene'][2]
        probabilities[person]['gene'][1] = alpha1 * probabilities[person]['gene'][1]
        probabilities[person]['gene'][0] = alpha1 * probabilities[person]['gene'][0]
        probabilities[person]['trait'][False] = alpha2* probabilities[person]['trait'][False]
        probabilities[person]['trait'][True] = alpha2* probabilities[person]['trait'][True]


if __name__ == "__main__":
    main()
