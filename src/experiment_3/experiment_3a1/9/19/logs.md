# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP
PROBLEM INFO:

- A food is manufactured by refining raw oils and blending them together. 
- The raw oils are either vegetable oils or non-vegetable oils. 
- Each oil \var{i} may be purchased in month \var{m} for price \var{price_{i,m}}.
- The final product sells at \var{sell_price} per ton.
- Vegetable oils and non-vegetable oils require different production lines for refining. 
- In any month, it is not possible to refine more than \var{max_vegetable_refining_per_month} tons of vegetable oils and more than \var{max_non_vegetable_refining_per_month} tons of non-vegetable oils. 
- There is no loss of weight in the refining process, and the cost of refining may be ignored.
- It is possible to store up to \var{storage_size} tons of each raw oil for use later. 
- The cost of storage for both vegetable and non-vegetable oil is \var{storage_cost} per ton per month.
- The final product cannot be stored, nor can refined oils be stored.
- There is a technological restriction of hardness on the final product. 
- In the units in which hardness is measured, this must lie between \var{max_hardness} and \var{min_hardness}.
- The hardness product is computed by the weighted average of hardness of each oil.
- The hardness of oil \var{i} is \var{hardness_{i}}.
- At present, there are \var{init_amount} tons of each type of raw oil in storage. 
- We can assume that there is a month "0" to model the inital amount.
- It is required that at the end of the last month, we still have the same amout of storage as \var{init_amount}.
- This means directly adding the constraint that the storage in the last month must be equal to \var{init_amount}.
- The food may never be made up of more than three oils in any month.
- If an oil is used in a month, at least \var{min_usage} tons must be used.
- There are dependencies in the oil usage and \var{dependency_{i, j}} shows this relation
- If \var{dependency_{i, j}} is 1, then when oil \var{i} is used, oil \var{j} must also be used


INPUT FORMAT:

{
    "buy_price":[[price_{i, m} for i in 1,...,I] for m in 1,...,M],
    "sell_price": sell_price,
    "is_vegetable": [is_vegetable_{i} for i in 1,...,I],
    "max_vegetable_refining_per_month": max_veg,
    "max_non_vegetable_refining_per_month": max_non_veg,
    "storage_size": storage_size,
    "storage_cost": storage_cost,
    "max_hardness": max_hardness,
    "min_hardness": min_hardness,
    "hardness": [hardness_{i} for i in 1,...,I],
    "init_amount": init_amount,
    "min_usage": min_usage,
    "dependencies": [dependency_{i} for i in 1,...,I]
}


OBJECTIVE: What buying, storing and manufacturing policy should the company pursue in order to maximize profit?

OUTPUT INFO: 

- \var{buyquantity} represents the amount of buying quantity of each oil in each month
- \var{refine} represents the amount of refined quantity of each oil in each month
- \var{storage} represents the storage of each oil in each month
 
OUTPUT FORMAT: 

{
    "buy": [[buyquantity_{i, m} for i in 1,...,I] for m in 1,...M],
    "refine": [[refine_{i, m} for i in 1,...,I] for m in 1,...M],
    "storage": [[storage_{i, m} for i in 1,...,I] for m in 1,...,M]
} 
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Oil Production}

\subsection*{Parameters}
\begin{itemize}
    \item $I$: Number of oils
    \item $M$: Number of months
    \item $price_{i,m}$: Purchase price of oil $i$ in month $m$
    \item $sell\_price$: Selling price of the final product per ton
    \item $is\_vegetable_{i}$: Indicator if oil $i$ is vegetable or not
    \item $max\_veg$: Maximum vegetable refining capacity per month
    \item $max\_non\_veg$: Maximum non-vegetable refining capacity per month
    \item $storage\_size$: Maximum storage capacity per oil
    \item $storage\_cost$: Cost of storing one ton of oil per month
    \item $max\_hardness$: Maximum allowable hardness of the final product
    \item $min\_hardness$: Minimum allowable hardness of the final product
    \item $hardness_{i}$: Hardness of oil $i$
    \item $init\_amount$: Initial storage amount of each oil
    \item $min\_usage$: Minimum required usage of each oil if used
    \item $dependency_{i,j}$: Dependency between oils $i$ and $j$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $buyquantity_{i,m}$: Amount of oil $i$ purchased in month $m$
    \item $refine_{i,m}$: Amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: Amount of oil $i$ stored at the end of month $m$
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}
1. **Storage constraint**:
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, m \quad (1 \leq m \leq M)
\]
where \(storage_{i,0} = init\_amount\).

2. **Refining capacity constraints**:
\[
\sum_{i \in V} refine_{i,m} \leq max\_veg, \quad \forall m \quad (1 \leq m \leq M)
\]
\[
\sum_{i \in NV} refine_{i,m} \leq max\_non\_veg, \quad \forall m \quad (1 \leq m \leq M)
\]
where \(V\) is the set of vegetable oils and \(NV\) is the set of non-vegetable oils.

3. **Hardness constraint**:
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m \quad (1 \leq m \leq M)
\]

4. **Storage limit constraint**:
\[
0 \leq storage_{i,m} \leq storage\_size, \quad \forall i, m \quad (1 \leq m \leq M)
\]

5. **Final month's storage constraint**:
\[
storage_{i,M} = init\_amount, \quad \forall i
\]

6. **Usage dependency constraint**:
If \(refine_{i,m} > 0\) then \(refine_{j,m} > 0\) if \(dependency_{i,j} = 1\).

7. **Minimum usage constraint**:
If \(refine_{i,m} > 0\) then \(refine_{i,m} \geq min\_usage, \quad \forall i, m \quad (1 \leq m \leq M)\)

8. **Oil usage constraint**:
At most 3 oils can be used per month:
\[
\sum_{i=1}^{I} \text{1}_{(refine_{i,m} > 0)} \leq 3, \quad \forall m \quad (1 \leq m \leq M)
\]

\subsection*{Conclusion}
This LP model captures the problem constraints and objectives, enabling the company to determine an optimal buying, storing, and manufacturing policy to maximize profits in the oil refining process.

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Oil Production}

\subsection*{Parameters}
\begin{itemize}
    \item $I$: Number of oils
    \item $M$: Number of months
    \item $price_{i,m}$: Purchase price of oil $i$ in month $m$
    \item $sell\_price$: Selling price of the final product per ton
    \item $is\_vegetable_{i}$: Indicator if oil $i$ is vegetable or not
    \item $max\_veg$: Maximum vegetable refining capacity per month
    \item $max\_non\_veg$: Maximum non-vegetable refining capacity per month
    \item $storage\_size$: Maximum storage capacity per oil
    \item $storage\_cost$: Cost of storing one ton of oil per month
    \item $max\_hardness$: Maximum allowable hardness of the final product
    \item $min\_hardness$: Minimum allowable hardness of the final product
    \item $hardness_{i}$: Hardness of oil $i$
    \item $init\_amount$: Initial storage amount of each oil
    \item $min\_usage$: Minimum required usage of each oil if used
    \item $dependency_{i,j}$: Dependency between oils $i$ and $j$
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $buyquantity_{i,m}$: Amount of oil $i$ purchased in month $m$
    \item $refine_{i,m}$: Amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: Amount of oil $i$ stored at the end of month $m$
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}
1. **Storage constraint**:
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, m \quad (1 \leq m \leq M)
\]
where \(storage_{i,0} = init\_amount\).

2. **Refining capacity constraints**:
\[
\sum_{i \in V} refine_{i,m} \leq max\_veg, \quad \forall m \quad (1 \leq m \leq M)
\]
\[
\sum_{i \in NV} refine_{i,m} \leq max\_non\_veg, \quad \forall m \quad (1 \leq m \leq M)
\]
where \(V\) is the set of vegetable oils and \(NV\) is the set of non-vegetable oils.

3. **Hardness constraint**:
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m \quad (1 \leq m \leq M)
\]

4. **Storage limit constraint**:
\[
0 \leq storage_{i,m} \leq storage\_size, \quad \forall i, m \quad (1 \leq m \leq M)
\]

5. **Final month's storage constraint**:
\[
storage_{i,M} = init\_amount, \quad \forall i
\]

6. **Usage dependency constraint**:
If \(refine_{i,m} > 0\) then \(refine_{j,m} > 0\) if \(dependency_{i,j} = 1\).

7. **Minimum usage constraint**:
If \(refine_{i,m} > 0\) then \(refine_{i,m} \geq min\_usage, \quad \forall i, m \quad (1 \leq m \leq M)\)

8. **Oil usage constraint**:
At most 3 oils can be used per month:
\[
\sum_{i=1}^{I} \text{1}_{(refine_{i,m} > 0)} \leq 3, \quad \forall m \quad (1 \leq m \leq M)
\]

\subsection*{Conclusion}
This LP model captures the problem constraints and objectives, enabling the company to determine an optimal buying, storing, and manufacturing policy to maximize profits in the oil refining process.

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

#### Define the problem
I = len(data['buy_price'])  #### Number of oils
M = len(data['buy_price'][0])  #### Number of months
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']
is_vegetable = data['is_vegetable']

problem = pulp.LpProblem("OilProduction", pulp.LpMaximize)

#### Create decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M)) - \
         storage_cost * pulp.lpSum(storage[i, m] for i in range(I) for m in range(M))

problem += profit

#### Storage constraint
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]

#### Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

#### Hardness constraint
for m in range(M):
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += total_refine > 0  #### To avoid division by zero
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine >= min_hardness
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / total_refine <= max_hardness

#### Final month's storage constraint
for i in range(I):
    problem += storage[i, M-1] == init_amount

#### Usage dependency constraint
for m in range(M):
    for i in range(I):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[i, m] <= refine[j, m]  #### If i is used, j must be used

#### Minimum usage constraint
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * pulp.lpSum(1 if refine[i, m] > 0 else 0 for m in range(M))

#### Oil usage constraint
for m in range(M):
    problem += pulp.lpSum(1 for i in range(I) if refine[i, m] > 0) <= 3

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

