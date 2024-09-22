# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A small electric utility operates \var{P} power plants to supply electricity to \var{C} cities.
- Each power plant has a capacity of \var{supply_{p}} million kwh.
- Each city has a peak demand of \var{demand_{c}} million kwh, which must be met at the same time.
- Power plant \var{p} can send electricity to city \var{c} at a transmission cost of \var{transmission_{p,c}} $/million kwh.

INPUT FORMAT: 

{
    "supply": [supply_{p} for p in 1, ..., P],
    "demand": [demand_{c} for c in 1, ..., C],
    "transmission_costs": [[transmission_{p,c} for c in 1, ..., C] for p in 1, ..., P]
}

OBJECTIVE: How much electricity should each power plant send to each city to minimize the total transmission cost?

OUTPUT INFO:

- the amount of electricity power plant \var{p} sends to city \var{c} as \var{send_{p,c}} million kwh.
- \var{total_cost} displays the total transmission cost for the utility.

OUTPUT FORMAT:

{
    "send": [[send_{p,c} for c in 1, ..., C] for p in 1, ..., P],
    "total_cost": total_cost
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Based on the provided problem description, here is the mathematical model for the linear programming problem to determine how much electricity each power plant should send to each city in order to minimize the total transmission cost:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item Let \( P \) be the set of power plants, indexed by \( p \).
    \item Let \( C \) be the set of cities, indexed by \( c \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{supply}_p \): The supply capacity of power plant \( p \) (in million kWh).
    \item \( \text{demand}_c \): The peak demand of city \( c \) (in million kWh).
    \item \( \text{transmission}_{p,c} \): The transmission cost from power plant \( p \) to city \( c \) (in dollars per million kWh).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{send}_{p,c} \): The amount of electricity sent from power plant \( p \) to city \( c \) (in million kWh).
\end{itemize}

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{Minimize} \quad \text{total\_cost} = \sum_{p \in P} \sum_{c \in C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Supply Constraint for each power plant:}
    \[
    \sum_{c \in C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p \in P
    \]
    This ensures that no power plant sends more electricity than its capacity.

    \item \textbf{Demand Constraint for each city:}
    \[
    \sum_{p \in P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c \in C
    \]
    This ensures that each city's demand is fully met.

    \item \textbf{Non-negativity Constraint:}
    \[
    \text{send}_{p,c} \geq 0, \quad \forall p \in P, \forall c \in C
    \]
    This ensures that negative electricity amounts are not possible.
\end{enumerate}

\end{document}
```

This model defines the optimization problem as minimizing the total transmission cost, subject to constraints ensuring that each power plant does not exceed its capacity and each city's demand is fully met. The solution to this model will provide the optimal amounts of electricity each power plant should send to each city.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item Let \( P \) be the set of power plants, indexed by \( p \).
    \item Let \( C \) be the set of cities, indexed by \( c \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{supply}_p \): The supply capacity of power plant \( p \) (in million kWh).
    \item \( \text{demand}_c \): The peak demand of city \( c \) (in million kWh).
    \item \( \text{transmission}_{p,c} \): The transmission cost from power plant \( p \) to city \( c \) (in dollars per million kWh).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{send}_{p,c} \): The amount of electricity sent from power plant \( p \) to city \( c \) (in million kWh).
\end{itemize}

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{Minimize} \quad \text{total\_cost} = \sum_{p \in P} \sum_{c \in C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Supply Constraint for each power plant:}
    \[
    \sum_{c \in C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p \in P
    \]
    This ensures that no power plant sends more electricity than its capacity.

    \item \textbf{Demand Constraint for each city:}
    \[
    \sum_{p \in P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c \in C
    \]
    This ensures that each city's demand is fully met.

    \item \textbf{Non-negativity Constraint:}
    \[
    \text{send}_{p,c} \geq 0, \quad \forall p \in P, \forall c \in C
    \]
    This ensures that negative electricity amounts are not possible.
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

#### Sets and indices
plants = range(len(data['supply']))
cities = range(len(data['demand']))

#### Create the LP problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

#### Decision variables
send = pulp.LpVariable.dicts("send", (plants, cities), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in plants for c in cities)

#### Constraints
#### Supply Constraint
for p in plants:
    problem += (pulp.lpSum(send[p][c] for c in cities) <= data['supply'][p], f"Supply_Constraint_Plant_{p}")

#### Demand Constraint
for c in cities:
    problem += (pulp.lpSum(send[p][c] for p in plants) == data['demand'][c], f"Demand_Constraint_City_{c}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

