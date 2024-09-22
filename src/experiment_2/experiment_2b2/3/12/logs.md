# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- Suppose that there are \var{N} available currencies, and assume that one unit of currency \var{i} can be exchanged for \var{rate_{i,j}} units of currency \var{j} (Naturally, we assume that \var{rate_{i,j}} > 0).
- There are also certain regulations that impose a limit \var{limit_i} on the total amount of currency \var{i} that can be exchanged (whether to other currencies or from other currencies) on any given day.
- Suppose that we start the day with \var{start_i} units of currency \var{i}
- Provide a linear programming formulation of this problem. Assume that for any sequence \var{i_1}, … ,\var{i_k} of currencies, we have \var{rate_{i_1,i_2}}, \var{rate_{i_2,i_3}}, ..., \var{rate_{i_{k-1}, i_{k}}, \var{rate_{i_k, i_1}} <= 1, which means that wealth cannot be multiplied by going through a cycle of currencies.

INPUT FORMAT: 

{
    "start": [start_i for i in 1, ..., N],
    "limit": [limit_i for i in 1, ..., N],
    "rate": [[rate_{i,j} for j in 1, ..., N] for i in 1, ..., N],
}

OBJECTIVE: The objective is to maximize the number of units of currency \var{N} that we end up with at the end of the day, through a sequence of currency transactions.

OUTPUT INFO: 

- The output json file contains a list of transactions, where each transaction is a json object with the following fields:
    - from: the currency that we are exchanging from
    - to: the currency that we are exchanging to
    - amount: the amount of currency that we are exchanging
- The output json file also contains the final amount of currency \var{N} that we end up with at the end of the day.

OUTPUT FORMAT: 

{
    "transactions": [
        {
            "from": i,
            "to": j,
            "amount": amount_{i,j}
        }
    ],
    "final_amount_of_currency_N": final_amount_of_currency_N
}
</DESCRIPTION>
<DATA>
{'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'N': 3, 
    'Start': [100.0, 50.0, 200.0], 
    'Limit': [1000.0, 200.0, 3000.0], 
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

#### Create LP problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

#### Decision variables
exchange = pulp.LpVariable.dicts("exchange", (
    (i, j) for i in range(N) for j in range(N) if i != j), lowBound=0)

#### Objective: Maximize the end amount of currency N
problem += pulp.lpSum(exchange[i, N-1] * rate[i][N-1] for i in range(N) if i != N-1)

#### Constraints
for i in range(N):
    #### Sum of currency exchanges from currency i should not exceed limit[i]
    problem += pulp.lpSum(exchange[i, j] for j in range(N) if i != j) <= limit[i]
    
    #### Balance equation for each currency i
    problem += start[i] + pulp.lpSum(exchange[j, i] * rate[j][i] for j in range(N) if i != j) - pulp.lpSum(exchange[i, j] for j in range(N) if i != j) >= 0

#### Solve the problem
problem.solve()

#### Extract results
transactions = [
    {"from": i, "to": j, "amount": pulp.value(exchange[i, j])}
    for i in range(N) for j in range(N) if i != j and pulp.value(exchange[i, j]) > 0
]

final_amount_of_currency_N = start[N-1] + pulp.lpSum(
    pulp.value(exchange[i, N-1]) * rate[i][N-1] for i in range(N) if i != N-1)

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

