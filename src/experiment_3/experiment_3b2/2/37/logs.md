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
To formulate the given problem as a linear programming model, we define the decision variables, objective function, and constraints based on the provided inputs and requirements:

**Decision Variables:**
- Let \( x_k \) represent the quantity of spare part \( k \) to be produced, where \( k = 1, \ldots, K \).

**Objective Function:**
- We want to maximize the total profit from producing the spare parts. This is given by the sum of the profit from each part multiplied by the quantity produced.

**Constraints:**
- For each shop \( s \), the total worker-hours for all parts should not exceed the shop's capacity.

The linear programming model can then be formulated as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Decision Variables:}
\[
x_k \geq 0, \quad \text{for } k = 1, \ldots, K
\]

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\textbf{Constraints:}
\[
\sum_{k=1}^{K} \text{time}_{k,s} \times x_k \leq \text{capacity}_{s}, \quad \text{for } s = 1, \ldots, S
\]

\end{document}
```

**Explanation:**
- The objective function \( Z \) represents the total profit, calculated by summing up the profit for each part type \( k \) multiplied by the number of parts produced \( x_k \).
- The constraints ensure that the total worker-hours used in each shop \( s \) for the production of all parts does not exceed the available capacity \( \text{capacity}_s \).
- The non-negativity constraints on \( x_k \) ensure that the quantities of parts produced are non-negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\textbf{Decision Variables:}
\[
x_k \geq 0, \quad \text{for } k = 1, \ldots, K
\]

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

\textbf{Constraints:}
\[
\sum_{k=1}^{K} \text{time}_{k,s} \times x_k \leq \text{capacity}_{s}, \quad \text{for } s = 1, \ldots, S
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

#### Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']
K = len(profit)  #### Number of decision variables
S = len(capacity)  #### Number of constraints

#### Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Objective"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

