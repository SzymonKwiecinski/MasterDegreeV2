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
To formulate this linear programming problem in LaTeX, we aim to maximize the profit from manufacturing spare automobile parts, subject to shop capacity constraints. We'll utilize the given inputs: times required in each shop for each part, profit per part, and shop capacity limits.

Let's assume:
- \( K \) is the number of different spare parts.
- \( S \) is the number of shops.
- \( \text{time}_{k,s} \) is the required worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \) is the profit for each part \( k \).
- \( \text{capacity}_{s} \) is the working hours capacity of shop \( s \).
- \( \text{quantity}_{k} \) is the decision variable representing the amount of spare part \( k \) to be made.

The linear programming model can be expressed as:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Maximize the profit function
\[
Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Subject to:}

For each shop \( s \), the capacity constraint is given by:
\[
\sum_{k=1}^{K} \text{time}_{k,s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad s = 1, 2, \ldots, S
\]

Non-negativity constraint:
\[
\text{quantity}_{k} \geq 0, \quad k = 1, 2, \ldots, K
\]

\end{document}
```

This model will determine the quantities of each spare part to maximize total profit while ensuring that the time spent in each shop does not exceed the shop's capacity.

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

Maximize the profit function
\[
Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Subject to:}

For each shop \( s \), the capacity constraint is given by:
\[
\sum_{k=1}^{K} \text{time}_{k,s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad s = 1, 2, \ldots, S
\]

Non-negativity constraint:
\[
\text{quantity}_{k} \geq 0, \quad k = 1, 2, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Initialize the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
quantity = pulp.LpVariable.dicts("Quantity", range(data['NumParts']), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * quantity[k] for k in range(data['NumParts'])), "Total_Profit"

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * quantity[k] for k in range(data['NumParts'])) <= data['Capacity'][s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

