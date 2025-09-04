import math
import random
import numpy as np
from matplotlib import pyplot as plt

# Parameters
a = 0.0085
n = 10000   
d = 50
newd = (math.log(1 / a)) ** 2

d1 = n - 1.1 * newd
d2 = d - 0.9 * newd
newn = 8 / math.log(1 / a)
n1 = n - 1.1 * newn
n2 = d - 0.9 * newn

m = int(n * (1 + a))   
candidates = list(range(m))
random.shuffle(candidates)

#Tier 1 from the pool of total candidates  
tier_size = n // 3  # Tier 1 size = 3333 candidates
tier_1 = candidates[:tier_size]   
pool = tier_1.copy()  # Working pool of Tier 1 candidates

unemployed = []
attempts = {i: set() for i in tier_1}  # Tracking attempts only for Tier 1 candidates
current_offer = ["N" for _ in range(n)]
number_applicants = [0 for _ in range(n)]

def process(i):
    global unemployed
    if len(attempts[i]) >= d:
        unemployed.append(i)

def Ber(p):
    return 1 if random.random() < p else 0

def choose_job(i):
    global attempts
    a = random.randint(0, n - 1)
    while a in attempts[i]:
        a = random.randint(0, n - 1)
    return a
 
i = 0
employed = []
remaining = pool[:]
while remaining:
    curr = remaining.pop(0)
    i += 1
    app = choose_job(curr)
    attempts[curr].add(app)
    number_applicants[app] += 1
    base_p = 0.9
    p = base_p / (number_applicants[app])
    p = min(1.0, max(0.01, p))
    if Ber(p) == 1:
        if current_offer[app] != "N":
            process(current_offer[app])
            if current_offer[app] in remaining:
                remaining.remove(current_offer[app])
        current_offer[app] = curr
        employed.append((curr, len(attempts[curr])))
    else:
        if len(attempts[curr]) < d:
            remaining.append(curr)
        else:
            process(curr)
 
total_attempts = sum(len(attempts[i]) for i in tier_1)
avg_applications_per_job = sum(number_applicants) / n
 
plt.figure(figsize=(12, 6))
 
attempts_counts = [len(attempts[i]) for i in tier_1]
max_attempts = max(attempts_counts)
 
unique_attempts, counts = np.unique(attempts_counts, return_counts=True)
 
plt.bar(unique_attempts, counts, color='blue', alpha=0.7, label='Number of Candidates')
 
plt.axvline(x=math.sqrt(d), color='red', linestyle='--', linewidth=1.5,
          label=f'√d ({math.sqrt(d):.1f})')
plt.axvline(x=d, color='green', linestyle=':', linewidth=1.5,
          label=f'Max Attempts (d={d})')

# Formatting
plt.title("Number of Attempts vs Number of Candidates (Tier 1)", fontsize=14)
plt.xlabel("Number of Attempts per Candidate", fontsize=12)
plt.ylabel("Number of Candidates", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, max_attempts + 1)
plt.xticks(np.arange(0, max_attempts + 2, 5))
plt.yticks(np.arange(0, max(counts) + 50, 50))
 
for x, y in zip(unique_attempts, counts):
    plt.text(x, y + 5, f'{y}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
