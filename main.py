# Quinten Reed
# U1L1
# Large Rat

from random import triangular, random, uniform, choice, shuffle
from time import time
from rat import Rat

GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def initial_population():
  '''Create the initial set of rats based on constants'''
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)
  
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1
  
    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)
  
  return rats

def calculate_weight(sex, mother, father):
  '''Generate the weight of a single rat'''
  
  if sex == "M":
    wt = int(triangular(mother.getWeight(), father.getWeight(), father.getWeight()))
  else:
    wt = int(triangular(mother.getWeight(), father.getWeight(), mother.getWeight()))
  
  return wt

def mutate(pups):
  """Check for mutability, modify weight of affected pups"""

  for item in pups[0] + pups[1]:
    if random() < MUTATE_ODDS:
      randomnum = uniform(MUTATE_MIN, MUTATE_MAX)
      item.mutate(randomnum)

  return pups

def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""

  shuffle(rats[0])

  children = [[], []]

  for i in range(len(rats[0])):
    for j in range(8):
      sex = choice(["M", "F"])
      weight = calculate_weight(sex, rats[1][i], rats[0][i])
      R = Rat(sex, weight)

      if sex == "M":
        children[0].append(R)
      else:
        children[1].append(R)

  return children

def select(rats, pups):
  '''Choose the largest viable rats for the next round of breeding'''


  if pups == [[], []]:
    rats2 = [rats[0], rats[1]]
  else:
    rats2 = [rats[0].extend(pups[0]), rats[1].extend(pups[1])]

  rats[0].sort(reverse=True)
  rats[1].sort(reverse=True)

  newrats = [[], []]

  for item in rats[0]:
    if item.canBreed() and len(newrats[0]) <= 10:
      newrats[0].append(item)

  for item in rats[1]:
    if item.canBreed() and len(newrats[1]) <= 10:
      newrats[1].append(item)

  if rats[0][0] < rats[1][0]:
    largest = rats[1][0]
  elif rats[0][0] >= rats[1][0]:
    largest = rats[0][0]

  return newrats, largest

def calculate_mean(rats):
  '''Calculate the mean weight of a population'''

  sumWt = 0
  numRats = 0

  for item in rats[0] + rats[1]:
    sumWt += item.getWeight()
    numRats += 1

  return sumWt // numRats

def fitness(rats):
  """Determine if the target average matches the current population's average"""
  
  mean = calculate_mean(rats)

  return mean >= GOAL, mean

def main():
  begin_time = time()
  generation_weight = []
  rats = initial_population()
  loop = 0
  fitness_bool = False
  children = [[], []]

  while not fitness_bool and loop < GENERATION_LIMIT:
    loop += 1
    fitness_bool, mean = fitness(rats)
    generation_weight.append(str(mean))
    rats, largest = select(rats, children)
    children = breed(rats)
    children = mutate(children)

  end_time = time()
  
  print("RESULTS".center(50, "~") + "\n")
  print(f"Final population mean: {mean}\n")
  print(f"Generations: {loop}")
  print(f"Experiment duration: ~{round(loop / GENERATIONS_PER_YEAR)} years")
  print(f"Simulation duration: ~{round(end_time - begin_time, 3)} seconds\n")
  print(f"Largest rat: {largest}\n\n")
  print("Generation weight averages:")
  gen_weight_text = ""

  for i in range(len(generation_weight)):
    if i % 10 == 0:
      print(gen_weight_text)
      gen_weight_text = ""

    gen_weight_text += generation_weight[i] + "\t"

  if gen_weight_text != "":
    print(gen_weight_text)

if __name__ == "__main__":
  main()