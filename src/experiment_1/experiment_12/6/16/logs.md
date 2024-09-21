# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for Electricity Distribution}

\subsection*{Objective}
Minimize the total transmission cost from power plants to cities.

\begin{equation}
\text{Minimize} \quad Z = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{TransmissionCosts}_{pc} \cdot x_{pc}
\end{equation}

\subsection*{Constraints}

\begin{align}
& \text{1. Each power plant has a limited supply capacity:} \nonumber \\
& \sum_{c=1}^{C} x_{pc} \leq \text{Supply}_p \quad \forall p = 1, \ldots, P \\
& \text{2. Each city has a specific electricity demand:} \nonumber \\
& \sum_{p=1}^{P} x_{pc} = \text{Demand}_c \quad \forall c = 1, \ldots, C \\
& \text{3. Electricity sent from any power plant to any city is non-negative:} \nonumber \\
& x_{pc} \geq 0 \quad \forall p = 1, \ldots, P, \; \forall c = 1, \ldots, C
\end{align}

\subsection*{Parameters}

\begin{itemize}
    \item $P$: Number of power plants (constant)
    \item $C$: Number of cities (constant)
    \item $\text{Supply}_p$: Electricity supply capacity of power plant $p$, for $p = 1, \ldots, P$
    \item $\text{Demand}_c$: Electricity demand of city $c$, for $c = 1, \ldots, C$
    \item $\text{TransmissionCosts}_{pc}$: Transmission cost from power plant $p$ to city $c$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $x_{pc}$: Amount of electricity transmitted from power plant $p$ to city $c$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the input data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

#### Number of power plants (P) and cities (C)
P = len(data['supply'])
C = len(data['demand'])

#### Decision variables x_pc (amount of electricity transmitted from plant p to city c)
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

#### Initialize the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

#### Objective function: Minimize the total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

#### Constraints

#### 1. Each power plant has a limited supply capacity
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Plant_{p}"

#### 2. Each city has a specific electricity demand
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

