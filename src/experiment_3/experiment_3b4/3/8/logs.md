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
To formulate the given problem as a Linear Programming (LP) model, we will define the decision variables, objective function, and constraints based on the provided information. 

The decision variables are the quantities of each spare part to be made, denoted as \( \text{{quantity}}_k \) for \( k = 1, \ldots, K \). 

The objective is to maximize the total profit, which is the sum of profit from each part multiplied by the quantity produced. 

The constraints ensure that the total worker-hours used in each shop does not exceed its capacity.

Let's define this LP model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Parts Production}

\textbf{Decision Variables:} \\
Let \( \text{quantity}_k \) be the number of units of part \( k \) to be produced, for \( k = 1, \ldots, K \).

\textbf{Objective Function:} \\
Maximize the total profit:
\[
\text{maximize} \quad \sum_{k=1}^{K} \text{profit}_k \cdot \text{quantity}_k
\]

\textbf{Constraints:} \\
For each shop \( s = 1, \ldots, S \), the total worker-hours required should not exceed the capacity:
\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot \text{quantity}_k \leq \text{capacity}_s, \quad \forall s = 1, \ldots, S
\]

\textbf{Non-negativity Constraints:}
\[
\text{quantity}_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This LP model specifies that the goal is to maximize the total profit while ensuring that the production plan respects the capacity constraints for each shop. Each production quantity must also be non-negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Parts Production}

\textbf{Decision Variables:} \\
Let \( \text{quantity}_k \) be the number of units of part \( k \) to be produced, for \( k = 1, \ldots, K \).

\textbf{Objective Function:} \\
Maximize the total profit:
\[
\text{maximize} \quad \sum_{k=1}^{K} \text{profit}_k \cdot \text{quantity}_k
\]

\textbf{Constraints:} \\
For each shop \( s = 1, \ldots, S \), the total worker-hours required should not exceed the capacity:
\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot \text{quantity}_k \leq \text{capacity}_s, \quad \forall s = 1, \ldots, S
\]

\textbf{Non-negativity Constraints:}
\[
\text{quantity}_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

num_parts = data['NumParts']
num_machines = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

#### Define problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

#### Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(num_parts))

#### Constraints
for s in range(num_machines):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(num_parts)) <= capacity[s]

#### Solve problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

