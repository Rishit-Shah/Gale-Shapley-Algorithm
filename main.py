import random

a = 1

# Input data be
d_candidates_job_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]
n_jobs = 15  # Number of jobs

# Candidates
m = int(n_jobs * (1 + a))  # Number of candidates
unfilled_count = 0

# Initialize candidates
candidates_available = list(range(m))

# Total applications and blank candidates
total_applications = 0
blank = 0

# Random preference list of candidates
candidates_preference_list = [random.sample(range(n_jobs), n_jobs) for a_jobs in range(m)]

# Random preference list of jobs
jobs_preference_list = [random.sample(range(m), m) for a_jobs in range(n_jobs)]

# assignments
assigned_jobs = {}
assigned_candidates = {}

#for top candidates
top_candidates = {job: None for job in range(n_jobs)}
top_candidate_rank = {job: float('inf') for job in range(n_jobs)}  # Keeps track of the top candidate rank for each job

# Precompute candidate ranks for jobs where each job is key and each rank is value.
candidate_rank = [
    {job: rank for rank, job in enumerate(candidates_preference_list[candidate])}
    for candidate in range(m)
]

# Initialize job candidate lists to track the candidates for each job
job_candidate_lists = {job: [] for job in range(n_jobs)}

while candidates_available:
    assigned = False
    candidate_start = candidates_available.pop(0)
    candidates_list_pref = candidates_preference_list[candidate_start]  # Gets candidate's preferred list

    for j in candidates_list_pref:
        total_applications += 1

        # lets check job assignment
        if j not in assigned_jobs:  # If job is not yet assigned
            assigned_jobs[j] = candidate_start # assign candidate to job
            assigned_candidates[candidate_start] = j  # assign job to candidate
            top_candidates[j] = candidate_start # candidates gets the job
            top_candidate_rank[j] = candidate_rank[candidate_start][j] #top candidate for job
            job_candidate_lists[j].append(candidate_start) #updates the rank of candidate
            assigned = True
            break
        else:
            already_assigned_candidate = assigned_jobs[j]  # if candidate already assigned to the job
            if candidate_rank[candidate_start][j] < candidate_rank[already_assigned_candidate][j]: # if rank of current candiadte is less
                assigned_jobs[j] = candidate_start # set new candidate to job and vice versa
                assigned_candidates[candidate_start] = j
                assigned_candidates[already_assigned_candidate] = None # make old candidate none and send it back to available candidates list
                candidates_available.append(already_assigned_candidate)
                top_candidates[j] = candidate_start
                top_candidate_rank[j] = candidate_rank[candidate_start][j]
                job_candidate_lists[j].remove(already_assigned_candidate) # remove old candidate
                job_candidate_lists[j].append(candidate_start) # add the new candidate to job's list
                assigned = True
                break
            else:
                if len(job_candidate_lists[j]) < n_jobs:  # checks for more or less than required number of candidates, if more then put it randomly inside
                    insert_pos = random.randint(0, len(job_candidate_lists[j]))
                    job_candidate_lists[j].insert(insert_pos, candidate_start)
                    assigned = True
                    break

    if not assigned:  #if candidate is not having any assigned job, make it blank.
        blank += 1

# Output results
print("Unfilled jobs:", unfilled_count)
print("Total applications:", total_applications)
print("Blank candidates:", blank)

# Print top candidates
for job in range(n_jobs):
    candidate = top_candidates[job]
    if candidate is not None:
        print(f"Job {job} - Top candidate: {candidate}")
    else:
        print(f"Job {job} - No top candidate assigned")
