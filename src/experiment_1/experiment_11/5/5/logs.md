# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for School Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $S$: Total number of schools
    \item $G$: Total number of student groups
    \item $N$: Total number of neighborhoods
    \item $Capacity_{s,g}$: Capacity of school $s$ for student group $g$, for $s = 1, \ldots, S$ and $g = 1, \ldots, G$
    \item $Population_{n,g}$: Population of student group $g$ in neighborhood $n$, for $n = 1, \ldots, N$ and $g = 1, \ldots, G$
    \item $Distance_{n,s}$: Distance between neighborhood $n$ and school $s$, for $n = 1, \ldots, N$ and $s = 1, \ldots, S$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_{n,g,s}$: Number of students from group $g$ in neighborhood $n$ assigned to school $s$
\end{itemize}

\subsection*{Objective Function}
Minimize the total distance traveled by all students:
\[
\min \sum_{n=1}^{N} \sum_{g=1}^{G} \sum_{s=1}^{S} Distance_{n,s} \cdot x_{n,g,s}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Total number of students from each student group $g$ assigned from neighborhood $n$ to schools does not exceed the population of group $g$ in neighborhood $n$:
    \[
    \sum_{s=1}^{S} x_{n,g,s} \leq Population_{n,g} \quad \forall n = 1, \ldots, N, \forall g = 1, \ldots, G
    \]
    
    \item Total number of students from each student group $g$ assigned to school $s$ does not exceed the capacity of school $s$ for student group $g$:
    \[
    \sum_{n=1}^{N} x_{n,g,s} \leq Capacity_{s,g} \quad \forall s = 1, \ldots, S, \forall g = 1, \ldots, G
    \]
    
    \item Each student is assigned to exactly one school:
    \[
    \sum_{s=1}^{S} x_{n,g,s} = Population_{n,g} \quad \forall n = 1, \ldots, N, \forall g = 1, \ldots, G
    \]
    
    \item All populations, capacities, and distances are non-negative:
    \[
    x_{n,g,s} \geq 0 \quad \forall n = 1, \ldots, N, \forall g = 1, \ldots, G, \forall s = 1, \ldots, S
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON format
data = {'S': 3, 'G': 2, 'N': 4, 
        'Capacity': [[15, 20], [20, 15], [5, 17]], 
        'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
        'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], 
                     [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

#### Parameters
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

#### Decision Variables
x = pulp.LpVariable.dicts('x', (range(N), range(G), range(S)), lowBound=0, cat='Continuous')

#### Problem Definition
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum(distance[n][s] * x[n][g][s] for n in range(N) for g in range(G) for s in range(S)), "Total_Distance"

#### Constraints
#### 1. Total number of students from each student group g assigned from neighborhood n does not exceed population
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) <= population[n][g], f"Population_Constraint_{n}_{g}"

#### 2. Total number of students from each student group g assigned to school s does not exceed capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_{s}_{g}"

#### 3. Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) == population[n][g], f"Assignment_Constraint_{n}_{g}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

