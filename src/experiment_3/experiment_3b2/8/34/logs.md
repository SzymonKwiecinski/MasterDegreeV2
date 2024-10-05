# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this linear programming problem, we will create a model to minimize the total cost of purchasing foods while satisfying the nutritional requirements. Below is the mathematical formulation of the problem in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Objective:} Minimize the total cost of purchasing foods.

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad \forall m = 1,\ldots,M
\]

\[
\text{quantity}_k \geq 0, \quad \forall k = 1,\ldots,K
\]

\textbf{Where:}
\begin{itemize}
    \item \(\text{price}_k\) is the price per unit of food \(k\).
    \item \(\text{demand}_m\) is the minimum required units of nutrient \(m\).
    \item \(\text{nutri}_{k, m}\) is the amount of nutrient \(m\) contained in one unit of food \(k\).
    \item \(\text{quantity}_k\) is the decision variable representing the quantity of food \(k\) to purchase.
\end{itemize}

\end{document}
```

This formulation consists of:

1. **Objective Function**: Minimize the total cost `Z` by choosing quantities of each food item, weighted by their respective prices.

2. **Constraints**: 
    - Ensure that the sum of nutrients provided by all chosen foods meets or exceeds the required amount for each nutrient.
    - Quantities of food must be non-negative.

3. **Decision Variables**: `quantity_k` for each food item \(k\).

This model can be solved using Linear Programming solvers to obtain the optimal quantities of each food that minimizes the cost while meeting nutritional requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Objective:} Minimize the total cost of purchasing foods.

\[
\text{Minimize } Z = \sum_{k=1}^{K} \text{price}_k \cdot \text{quantity}_k
\]

\textbf{Subject to:}

\[
\sum_{k=1}^{K} \text{nutri}_{k, m} \cdot \text{quantity}_k \geq \text{demand}_m, \quad \forall m = 1,\ldots,M
\]

\[
\text{quantity}_k \geq 0, \quad \forall k = 1,\ldots,K
\]

\textbf{Where:}
\begin{itemize}
    \item \(\text{price}_k\) is the price per unit of food \(k\).
    \item \(\text{demand}_m\) is the minimum required units of nutrient \(m\).
    \item \(\text{nutri}_{k, m}\) is the amount of nutrient \(m\) contained in one unit of food \(k\).
    \item \(\text{quantity}_k\) is the decision variable representing the quantity of food \(k\) to purchase.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}
price = data['price']
demand = data['demand']
nutrition = data['nutrition']
K = len(price)  #### Number of food items
M = len(demand)  #### Number of nutrients

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

#### Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

#### Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Demand_Constraint_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

