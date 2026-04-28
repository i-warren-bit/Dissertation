import numpy as np
import matplotlib.pyplot as plt

def simulate_gbm(s0, mu, sigma, n_steps, n_simulations,T=1):
   
    dt = 1 / n_steps  # Time step

    W = np.random.normal(loc=0,size=(n_steps, n_simulations))

    
    price_factors = np.zeros((n_steps, n_simulations))
    S=np.zeros((n_steps, n_simulations))
    S[0,:] = s0

    for i in range(n_steps):
        for j in range(n_simulations):
            price_factors[i,j] = np.exp((mu-0.5*sigma**2)*dt+np.sqrt(dt)*sigma*W[i,j])
    
    
    time_points = np.linspace(0, 1, n_steps)
    for i in range(n_steps-1):
        S[i+1,:] = S[i,:] * price_factors[i,:]
        
    
    return time_points, S
    


initial_price = 100  # Initial stock price
expected_return = 0.1171 # Annual expected return (10%)
standard_deviation = 0.15  
num_steps = 250  # Number of trading days in a year
num_simulations = 10

time, paths = simulate_gbm(initial_price, expected_return, standard_deviation, num_steps, num_simulations)

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(time, paths)
#plt.title('Geometric Brownian Motion Simulation for Stock Prices')
plt.xlabel('Time (Years)', size=12)
plt.ylabel('Stock Price', size=12)
plt.grid(True)
plt.show()


