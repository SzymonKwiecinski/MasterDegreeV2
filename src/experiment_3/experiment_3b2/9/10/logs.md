# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- Consider a school district with \var{N} neighborhoods, \var{S} schools, and \var{G} grades at each school.
- Each school \var{s} has a capacity of \var{capacity_{s,g}} for grade \var{g}. 
- In each neighborhood \var{n}, the student population of grade \var{g} is \var{population_{n,g}}. 
- Finally, the distance of school \var{s} from neighborhood \var{n} is \var{d_{i,j}}.

INPUT FORMAT: 

{
    "capacity": [[capacity_{s,g} for g in 1, ..., G] for s in 1, ..., S],
    "population": [[population_{n,g} for g in 1, ..., G] for n in 1, ..., N],
    "distance": [[d_{n,s} for s in 1, ..., S] for n in 1, ..., N]
}

OBJECTIVE: We want to assign all students to schools, while minimizing the total distance traveled by all students. We may ignore the fact that numbers of students must be integers.

OUTPUT INFO:
- the output should show optimal \var{x_{n,s,g}} for all \var{n}, \var{s}, \var{g} (i.e., the number of students of grade \var{g} in neighborhood \var{n} assigned to school \var{s}).
- the output should also include \var{total_distance}, the total distance traveled by all students.

OUTPUT FORMAT:

{
    "assignment": [[[x_{n,s,g} for g in 1, ..., G] for s in 1, ..., S] for n in 1, ..., N],
    "total_distance": total_distance
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we'll formulate it as a Linear Programming (LP) problem with the objective of minimizing the total distance traveled by all students. The decision variables will represent the number of students from each neighborhood and grade assigned to each school.

######### Objective Function:
Minimize the total travel distance:
\[
\text{minimize} \quad \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

######### Constraints:
1. **Capacity Constraint for each school and grade:**
   \[
   \sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
   \]

2. **Population Constraint for each neighborhood and grade:**
   \[
   \sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
   \]

3. **Non-negativity Constraint:**
   \[
   x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
   \]

Here's the corresponding LaTeX code:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for Student Assignment Problem}

\textbf{Objective:}

Minimize the total distance:
\[
\text{minimize} \quad \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\textbf{Subject to:}

Capacity constraints for each school and grade:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

Population constraints for each neighborhood and grade:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
\]

Non-negativity constraints:
\[
x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

\end{document}
```

This setup will give you the optimal assignment of students to schools that minimizes travel distance while respecting both school capacities and neighborhood populations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for Student Assignment Problem}

\textbf{Objective:}

Minimize the total distance:
\[
\text{minimize} \quad \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\textbf{Subject to:}

Capacity constraints for each school and grade:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

Population constraints for each neighborhood and grade:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
\]

Non-negativity constraints:
\[
x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data in json format
data = json.loads('{"S": 3, "G": 2, "N": 4, "Capacity": [[15, 20], [20, 15], [5, 17]], "Population": [[7, 19], [4, 12], [9, 2], [6, 8]], "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}')

#### Extracting data from JSON
S = data['S']  #### Number of schools
G = data['G']  #### Number of grades
N = data['N']  #### Number of neighborhoods
capacity = data['Capacity']  #### Capacity constraints
population = data['Population']  #### Population requirements
distance = data['Distance']  #### Distance matrix

#### Create the problem
problem = pulp.LpProblem("Student_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

#### Objective function: Minimize total distance
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

#### Capacity constraints for each school and grade
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

#### Population constraints for each neighborhood and grade
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Population_Constraint_n{n}_g{g}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

