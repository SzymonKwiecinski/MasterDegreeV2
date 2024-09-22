# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small firm specializes in making some types of spare automobile parts. 
- Each part is has to go through several shops 
- The required worker-hours for part \var{k} in shop \var{s} is \var{time_{k, s}}.
- The profit of part \var{k} is \var{profit_{k}}.
- The capacity of shop \var{s} is \var{capacity_{s}} working hours.

INPUT FORMAT:

{
	"time": [[time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"profit": [profit_{k} for k in 1,...,K],
	"capacity": [capacity_{s} for s in 1,...,S]
}


OBJECTIVE: Formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit.

OUTPUT INFO:

- \var{quantity} represents the amount of each spare part to be made

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the given problem as a Linear Programming (LP) model, we need to determine the quantities of each spare part to be made such that the total profit is maximized, while respecting the constraints of available work hours in each shop. This leads us to the following LP model:

Let:
- \( K \) be the number of spare parts.
- \( S \) be the number of shops.
- \( \text{time}_{k,s} \) be the worker-hours required for part \( k \) in shop \( s \).
- \( \text{profit}_k \) be the profit for producing one unit of part \( k \).
- \( \text{capacity}_s \) be the available working hours in shop \( s \).

Define:
- \( \text{quantity}_k \) as the decision variable representing the amount of part \( k \) to be produced, for \( k = 1, \ldots, K \).

The objective is to maximize the total profit:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times \text{quantity}_k
\]

Subject to the constraints:

1. For each shop \( s \), the total worker-hours required must not exceed the available capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \times \text{quantity}_k \leq \text{capacity}_s, \quad \text{for } s = 1, \ldots, S
\]

2. The quantities of each spare part must be non-negative:

\[
\text{quantity}_k \geq 0, \quad \text{for } k = 1, \ldots, K
\]

Below is the Linear Programming model written in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the profit: 
\[
Z = \sum_{k=1}^{K} \text{profit}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}

For each shop \( s = 1, \ldots, S \):
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_k \leq \text{capacity}_s
\]

Non-negativity constraints for all parts \( k = 1, \ldots, K \):
\[
\text{quantity}_k \geq 0
\]

\end{document}
```

This represents the complete mathematical model for the problem described, with the objective function and constraints specified clearly.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the profit: 
\[
Z = \sum_{k=1}^{K} \text{profit}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}

For each shop \( s = 1, \ldots, S \):
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_k \leq \text{capacity}_s
\]

Non-negativity constraints for all parts \( k = 1, \ldots, K \):
\[
\text{quantity}_k \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Parameters
K = data['NumParts']  #### Number of parts
S = data['NumMachines']  #### Number of shops

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += (pulp.lpSum(data['Time'][k][s] * quantity[k] for k in range(K)) <= data['Capacity'][s]), f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

