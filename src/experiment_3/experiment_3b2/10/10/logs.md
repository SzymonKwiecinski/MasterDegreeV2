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
To solve this problem, we need to create a linear programming model that minimizes the total distance traveled by all students while satisfying the school capacity constraints and assigning all neighborhood students to schools.

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Indices:}
\begin{align*}
    n & \text{: Index for neighborhoods, } n = 1, \ldots, N \\
    s & \text{: Index for schools, } s = 1, \ldots, S \\
    g & \text{: Index for grades, } g = 1, \ldots, G \\
\end{align*}

\textbf{Parameters:}
\begin{align*}
    \text{capacity}_{s,g} & \text{: Capacity of school } s \text{ for grade } g, \\
    \text{population}_{n,g} & \text{: Population of students in neighborhood } n \text{ for grade } g, \\
    d_{n,s} & \text{: Distance from neighborhood } n \text{ to school } s. \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
    x_{n,s,g} & \text{: Number of students of grade } g \text{ from neighborhood } n \text{ assigned to school } s. \\
\end{align*}

\textbf{Objective:}
\begin{align*}
    \text{Minimize } & \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g} \\
\end{align*}

\textbf{Subject to:}
\begin{align*}
    & \sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, \forall g \quad & \text{(All students must be assigned)} \\
    & \sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, \forall g \quad & \text{(Capacity constraints)} \\
    & x_{n,s,g} \geq 0 \quad \forall n, \forall s, \forall g \quad & \text{(Non-negativity)}
\end{align*}

\end{document}
```

This model aims to minimize the total distance by assigning students to schools while ensuring all students are assigned and no school exceeds its capacity for any grade. The decision variable \( x_{n,s,g} \) represents the number of students from neighborhood \( n \) of grade \( g \) assigned to school \( s \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Indices:}
\begin{align*}
    n & \text{: Index for neighborhoods, } n = 1, \ldots, N \\
    s & \text{: Index for schools, } s = 1, \ldots, S \\
    g & \text{: Index for grades, } g = 1, \ldots, G \\
\end{align*}

\textbf{Parameters:}
\begin{align*}
    \text{capacity}_{s,g} & \text{: Capacity of school } s \text{ for grade } g, \\
    \text{population}_{n,g} & \text{: Population of students in neighborhood } n \text{ for grade } g, \\
    d_{n,s} & \text{: Distance from neighborhood } n \text{ to school } s. \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
    x_{n,s,g} & \text{: Number of students of grade } g \text{ from neighborhood } n \text{ assigned to school } s. \\
\end{align*}

\textbf{Objective:}
\begin{align*}
    \text{Minimize } & \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g} \\
\end{align*}

\textbf{Subject to:}
\begin{align*}
    & \sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, \forall g \quad & \text{(All students must be assigned)} \\
    & \sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, \forall g \quad & \text{(Capacity constraints)} \\
    & x_{n,s,g} \geq 0 \quad \forall n, \forall s, \forall g \quad & \text{(Non-negativity)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

#### Parameters
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

#### Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

#### Objective Function
problem = pulp.LpProblem("Minimize_Transportation_Costs", pulp.LpMinimize)
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

#### Constraints
#### All students must be assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Assign_Students_N{n}_G{g}"

#### Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_S{s}_G{g}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

