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
To model this problem as a Linear Programming (LP) problem, we will define decision variables, constraints, and the objective function using the information given. The goal is to assign students from neighborhoods to schools in a way that minimizes the total distance traveled while respecting the capacity constraints of each school.

######### Decision Variables
- Let \( x_{n,s,g} \) be the number of students of grade \( g \) from neighborhood \( n \) assigned to school \( s \).

######### Objective Function
- Minimize the total distance traveled by all students:
  \[
  \text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
  \]

######### Constraints
1. **Capacity Constraints:**
   Each school \( s \) must not exceed its capacity for each grade \( g \):
   \[
   \sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
   \]

2. **Population Constraints:**
   All students from each neighborhood \( n \) for each grade \( g \) must be assigned to some school:
   \[
   \sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
   \]

3. **Non-negativity Constraints:**
   The number of students assigned must be non-negative:
   \[
   x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
   \]

Now, let's put this into LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for School Assignment}

\subsection*{Objective}
Minimize the total distance traveled by all students:
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}
1. \textbf{Capacity Constraints:}
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

2. \textbf{Population Constraints:}
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
\]

3. \textbf{Non-negativity Constraints:}
\[
x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

\end{document}
```

This LaTeX model captures the constraints and the objective function required to solve the school assignment problem using linear programming techniques. The problem can then be solved using an LP solver to find the optimal values \( x_{n,s,g} \) and the total distance.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for School Assignment}

\subsection*{Objective}
Minimize the total distance traveled by all students:
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}
1. \textbf{Capacity Constraints:}
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
\]

2. \textbf{Population Constraints:}
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
\]

3. \textbf{Non-negativity Constraints:}
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

#### Data provided in JSON format
data = json.loads('{"S": 3, "G": 2, "N": 4, "Capacity": [[15, 20], [20, 15], [5, 17]], "Population": [[7, 19], [4, 12], [9, 2], [6, 8]], "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}')

#### Extracting data
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

#### Initialize the problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

#### Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(distance[n][g] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

#### Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_{s}_{g}"

#### Population constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Population_Constraint_{n}_{g}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

