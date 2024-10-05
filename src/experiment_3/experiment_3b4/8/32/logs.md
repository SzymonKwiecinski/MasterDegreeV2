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
To solve this linear programming problem, we need to determine the optimal quantities of products to produce in order to maximize profit, while ensuring that the production times at each stage do not exceed the available working hours. Here is the mathematical model represented in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}

Let:
\begin{align*}
    K & : \text{Number of products} \\
    S & : \text{Number of stages} \\
    \text{produce\_time}_{k, s} & : \text{Time to produce one unit of product } k \text{ at stage } s  \\
    \text{time}_{s} & : \text{Available working hours at stage } s \\
    \text{profit}_{k} & : \text{Unitary profit for product } k
\end{align*}

\subsection*{Decision Variables}

\begin{align*}
    \text{quantity}_{k} & : \text{Quantity to produce for product } k
\end{align*}

\subsection*{Objective Function}

Maximize the total profit:
\[
\max \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\subsection*{Constraints}

For each stage $s = 1, \ldots, S$:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times \text{quantity}_{k} \leq \text{time}_{s}
\]

Non-negativity constraints:
\[
\text{quantity}_{k} \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This model includes the following components:

1. **Parameters:**
   - `produce_time_{k, s}`: The time required to produce one unit of product k at stage s.
   - `time_{s}`: The total available time for stage s.
   - `profit_{k}`: The profit gained from each unit of product k.

2. **Decision Variables:**
   - `quantity_{k}`: The quantity of product k to be produced.

3. **Objective Function:**
   - We aim to maximize the total profit derived from all products.

4. **Constraints:**
   - Ensure the total production time for all products at each stage does not exceed the available working hours.
   - Include non-negativity constraints for the production quantities. 

You would need to provide the specific values for each parameter to solve this LP problem using any LP solver.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}

Let:
\begin{align*}
    K & : \text{Number of products} \\
    S & : \text{Number of stages} \\
    \text{produce\_time}_{k, s} & : \text{Time to produce one unit of product } k \text{ at stage } s  \\
    \text{time}_{s} & : \text{Available working hours at stage } s \\
    \text{profit}_{k} & : \text{Unitary profit for product } k
\end{align*}

\subsection*{Decision Variables}

\begin{align*}
    \text{quantity}_{k} & : \text{Quantity to produce for product } k
\end{align*}

\subsection*{Objective Function}

Maximize the total profit:
\[
\max \sum_{k=1}^{K} \text{profit}_{k} \times \text{quantity}_{k}
\]

\subsection*{Constraints}

For each stage $s = 1, \ldots, S$:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times \text{quantity}_{k} \leq \text{time}_{s}
\]

Non-negativity constraints:
\[
\text{quantity}_{k} \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define the data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Extract the data
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

#### Constraints for each stage
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in range(K)) <= available_time[s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

