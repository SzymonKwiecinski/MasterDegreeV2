import pulp
import json

def solve_currency_exchange_problem(data):
    N = data['N']
    start = data['Start']
    limit = data['Limit']
    rate = data['Rate']
    
    # Create a LP maximization problem
    problem = pulp.LpProblem("CurrencyExchangeProblem", pulp.LpMaximize)

    # Creating decision variables for amounts exchanged from currency i to j
    amounts = [[pulp.LpVariable(f'amount_{i}_{j}', lowBound=0) for j in range(N)] for i in range(N)]

    # Objective function: Maximize the final amount of currency N
    final_currency_N = start[-1] + sum(amounts[i][N-1] * rate[i][N-1] for i in range(N))
    problem += final_currency_N

    # Constraints for starting currency balance for each currency i
    for i in range(N):
        problem += start[i] - sum(amounts[i][j] for j in range(N)) + sum(amounts[j][i] * rate[j][i] for j in range(N)) <= limit[i]

    # Constraints for not over-exchanging each currency i
    for i in range(N):
        problem += sum(amounts[i][j] for j in range(N)) <= start[i] + sum(amounts[j][i] * rate[j][i] for j in range(N))
    
    # Solve the problem
    problem.solve()

    # Prepare the output in the desired format
    transactions = []
    for i in range(N):
        for j in range(N):
            if i != j:
                transaction_amount = pulp.value(amounts[i][j])
                if transaction_amount > 0:
                    transactions.append({
                        "from": i + 1,  # converting to 1-indexed
                        "to": j + 1,    # converting to 1-indexed
                        "amount": transaction_amount
                    })
    
    final_amount_of_currency_N = pulp.value(final_currency_N)
    
    # Output the result as JSON
    output = {
        "transactions": transactions,
        "final_amount_of_currency_N": final_amount_of_currency_N
    }
    
    print(json.dumps(output, indent=4))

    # Print the objective value
    print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Given data
data = {
    "N": 3,
    "Start": [100.0, 50.0, 200.0],
    "Limit": [1000.0, 200.0, 3000.0],
    "Rate": [
        [0.99, 0.9, 1.02],
        [0.95, 0.99, 0.92],
        [0.9, 0.91, 0.99]
    ]
}

solve_currency_exchange_problem(data)