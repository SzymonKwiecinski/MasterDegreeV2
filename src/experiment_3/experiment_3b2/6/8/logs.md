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
To formulate this problem as a Linear Programming (LP) model, we need to determine the production quantities of each spare part to maximize the firm's profit, subject to shop capacity constraints. Below is the mathematical model for the problem:

Given:

- \( K \): Number of different spare parts.
- \( S \): Number of different shops.
- \( \text{time}_{k, s} \): The required worker-hours for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \): The profit for producing one unit of part \( k \).
- \( \text{capacity}_{s} \): The capacity (in worker-hours) of shop \( s \).

Decision Variables:

- \( \text{quantity}_{k} \): Number of spare parts \( k \) to be produced.

The linear programming model can be formulated as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{time}_{k, s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

Explanation:
- The objective function aims to maximize total profit by summing the profits of all produced parts.
- The first set of constraints ensures that the total worker-hours used by any shop \( s \) does not exceed its capacity.
- The non-negativity constraints ensure that you cannot produce a negative quantity of any part.

This model should be implemented in a suitable optimization solver with the given input data format to find the optimal quantities of each spare part.

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
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{time}_{k, s} \times \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data initialization
data = json.loads('{"NumParts": 5, "NumMachines": 2, "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "Profit": [30, 20, 40, 25, 10], "Capacity": [700, 1000]}')

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
quantities = pulp.LpVariable.dicts("quantity", range(data['NumParts']), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * quantities[k] for k in range(data['NumParts'])), "Total_Profit"

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['Time'][k][s] * quantities[k] for k in range(data['NumParts'])) <= data['Capacity'][s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

