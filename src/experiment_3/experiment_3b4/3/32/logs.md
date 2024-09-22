# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We suppose that some products can be produced, each of them passing through several stages.
- Necessary time to produce 1 unit of product \var{k} is \var{produce_time_{k, s}} hours for stage \var{s}.
- Availability in working hours is \var{time_{s}} for stage \var{s}. 
- The unitary profits for product \var{k} is \var{profit_{k}}.

INPUT FORMAT:

{
	"produce_time": [[produce_time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"available_time": [time_{s} for s in 1,...,S],
	"profit": [profit_{k} for k in 1,...,K]
}


OBJECTIVE: Determine the quantities to be produced such that all the production constraints are satisfied and the profit is maximized.

OUTPUT INFO:

- \var{quantity} represents the production quantity for each product

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this linear programming problem, we need to formulate it using the given input. Our goal is to maximize the total profit by determining the optimal production quantities for each product, subject to the constraints on the available production time at each stage.

Here's the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
Maximize the total profit, which is given by:
\[
Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Constraints:}

1. Time constraints at each stage:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \times \text{quantity}_{k} \leq \text{time}_{s}, \quad \forall s = 1, \ldots, S
\]

2. Non-negativity constraints for each product:
\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\textbf{Variables:}
- \(\text{quantity}_{k}\): the number of units to produce for each product \(k\).

\end{document}
```

In this model:
- \(K\) is the number of products.
- \(S\) is the number of production stages.
- \(\text{produce\_time}_{k,s}\) is the time required to produce one unit of product \(k\) at stage \(s\).
- \(\text{time}_{s}\) is the total available time at stage \(s\).
- \(\text{profit}_{k}\) is the profit obtained from selling one unit of product \(k\).

This linear program can be solved using optimization software or solvers that handle linear programming problems.

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
Maximize the total profit, which is given by:
\[
Z = \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\textbf{Constraints:}

1. Time constraints at each stage:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \times \text{quantity}_{k} \leq \text{time}_{s}, \quad \forall s = 1, \ldots, S
\]

2. Non-negativity constraints for each product:
\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\textbf{Variables:}
- \(\text{quantity}_{k}\): the number of units to produce for each product \(k\).

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse the data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * quantities[k] for k in range(data['NumProducts'])), "Total Profit"

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * quantities[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s], f"Time_Constraint_Machine_{s}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

