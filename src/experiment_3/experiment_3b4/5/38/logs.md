# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small computer manufacturing company forecasts the demand over the next \var{n}-th month to be \var{demand_{n}}.
- These demands must be satisfied and can not be shorted.
- In any month it can produce at most \var{max_regular_amount} units, using regular production, at a cost of \var{cost_regular} dollars per unit. 
- By using overtime, it can produce additional units at \var{cost_overtime} dollars per unit. 
- The firm can store units from month to month at a cost of \var{store_cost} dollars per unit per month. 

INPUT FORMAT:

{
	"demand": [demand_{n} for n in 1,...,N],
	"max_regular_amount": max_regular_amount,
	"cost_regular": cost_regular,
	"cost_overtime": cost_overtime,
	"store_cost": store_cost
}


OBJECTIVE: Formulate the problem of determining the production schedule that minimizes the cost.

OUTPUT INFO:

- \var{reg_quant} represents the quantity of products produced using regular production in each future month
- \var{over_quant} represents the quantity of products produced using overtime production in each future month

OUTPUT FORMAT:

{
	"reg_quant": [reg_quant_{n} for n in 1,...,N]
	"over_quant": [over_quant_{n} for n in 1,...,N]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To create a linear programming model for the given problem, we need to define the decision variables, the objective function, and the constraints based on the provided input information. 

Let's define the variables:
- \( \text{reg\_quant}_{n} \): the quantity of products produced using regular production in month \( n \).
- \( \text{over\_quant}_{n} \): the quantity of products produced using overtime production in month \( n \).
- \( \text{store\_quant}_{n} \): the quantity of products stored at the end of month \( n \).

Objective Function: 
Minimize the total cost, which includes regular production cost, overtime production cost, and storage cost.

Constraints:
1. The production in regular time cannot exceed the maximum allowed regular production.
2. The sum of regular production, overtime production, and previous month's storage should satisfy the demand for each month.
3. Link the end-of-month inventory with storage for the next month.

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
Minimize the total cost:

\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot \text{reg\_quant}_{n} + \text{cost\_overtime} \cdot \text{over\_quant}_{n} + \text{store\_cost} \cdot \text{store\_quant}_{n} \right)
\]

\textbf{Subject to:}

1. \text{Regular Production Constraint:}
\[
0 \leq \text{reg\_quant}_{n} \leq \text{max\_regular\_amount} \quad \forall n = 1, \ldots, N
\]

2. \text{Demand Satisfaction Constraint:}
\[
\text{reg\_quant}_{n} + \text{over\_quant}_{n} + \text{store\_quant}_{n-1} = \text{demand}_{n} + \text{store\_quant}_{n} \quad \forall n = 1, \ldots, N
\]
\text{Note: Assume } \text{store\_quant}_{0} = 0 \text{ (no initial inventory)}

3. \text{Non-negativity Constraints:}
\[
\text{reg\_quant}_{n} \geq 0, \quad \text{over\_quant}_{n} \geq 0, \quad \text{store\_quant}_{n} \geq 0 \quad \forall n = 1, \ldots, N
\]

\end{document}
```

This model captures the need to satisfy the demand each month, considering the production and storage costs, while adhering to the production capacity constraints.

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
Minimize the total cost:

\[
\text{Minimize } Z = \sum_{n=1}^{N} \left( \text{cost\_regular} \cdot \text{reg\_quant}_{n} + \text{cost\_overtime} \cdot \text{over\_quant}_{n} + \text{store\_cost} \cdot \text{store\_quant}_{n} \right)
\]

\textbf{Subject to:}

1. \text{Regular Production Constraint:}
\[
0 \leq \text{reg\_quant}_{n} \leq \text{max\_regular\_amount} \quad \forall n = 1, \ldots, N
\]

2. \text{Demand Satisfaction Constraint:}
\[
\text{reg\_quant}_{n} + \text{over\_quant}_{n} + \text{store\_quant}_{n-1} = \text{demand}_{n} + \text{store\_quant}_{n} \quad \forall n = 1, \ldots, N
\]
\text{Note: Assume } \text{store\_quant}_{0} = 0 \text{ (no initial inventory)}

3. \text{Non-negativity Constraints:}
\[
\text{reg\_quant}_{n} \geq 0, \quad \text{over\_quant}_{n} \geq 0, \quad \text{store\_quant}_{n} \geq 0 \quad \forall n = 1, \ldots, N
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

#### Number of periods
N = len(data['demand'])

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=data['max_regular_amount'])
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
store_quant = pulp.LpVariable.dicts("store_quant", range(N), lowBound=0)

#### Objective function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store_quant[n]
    for n in range(N)
])

#### Constraints
#### Initial storage constraint
prev_store_quant = 0
for n in range(N):
    #### Demand Satisfaction Constraint
    problem += reg_quant[n] + over_quant[n] + prev_store_quant == data['demand'][n] + store_quant[n]
    
    #### Update the previous store quantity for the next period
    prev_store_quant = store_quant[n]

#### Solve the problem
problem.solve()

#### Output the optimal value of the objective function
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

