import numpy as np
import matplotlib.pyplot as plt

X=[271.86, 273.08, 273.76, 273.40, 273.81, 272.36, 270.97, 273.67, 272.19, 271.84, 274.61, 274.11, 278.28, 278.03, 278.78, 277.18, 277.89, 278.78, 280.70, 284.15, 286.19, 283.10, 278.85, 277.55, 276.97, 275.92, 271.49, 266.25, 268.56, 267.44, 267.46, 272.41, 272.95, 273.47, 275.25, 269.43, 268.47, 269.77, 270.14, 270.04, 269.05, 270.37, 271.40, 269.70, 269.00, 268.81, 262.82, 259.58, 258.45, 262.77, 262.24, 252.29, 247.45, 249.34, 247.77, 247.66, 245.27, 254.04, 258.06, 256.48, 256.69, 258.02, 257.13, 255.45, 254.63, 254.43, 255.46, 256.87, 252.31, 254.43, 256.08, 245.50, 237.88, 238.99, 238.15, 236.70, 234.07, 230.03, 226.79, 234.35, 237.88, 239.69, 239.78, 238.47, 229.72, 232.14, 232.56, 230.49, 229.31, 227.16, 227.76, 224.90, 226.01, 230.56, 230.89, 231.59, 232.78, 233.33, 229.65, 227.18, 229.35, 220.03, 213.25, 202.92, 203.35, 202.38, 207.57, 209.05, 211.27, 214.05, 213.88, 213.76, 214.15, 214.40, 212.48, 211.18, 210.02, 210.16, 209.11, 208.62, 211.16, 212.41, 211.14, 210.01, 209.95, 213.55, 212.44, 207.82, 205.17, 201.08, 201.00, 201.56, 200.30, 201.50, 201.00, 196.58, 195.64, 198.42, 196.45, 199.20, 198.78, 202.67, 201.45, 203.92, 200.63, 202.82, 203.27, 201.70, 200.85, 199.95, 200.42, 200.21, 195.27, 201.36, 202.09, 206.86, 208.78, 211.26, 211.45, 212.33, 212.93, 210.79, 198.53, 197.49, 196.25, 198.51, 198.89, 205.35, 213.32, 212.50, 211.21, 210.14, 209.28, 208.37, 204.60, 199.74, 193.16, 196.98, 194.27, 202.14, 202.52, 198.15, 190.42, 198.85, 172.42, 181.46, 188.38, 203.19, 223.89, 223.19, 222.13, 217.90, 223.85, 221.53, 223.75, 220.73, 218.27, 214.10, 215.24, 212.69, 214.00, 213.49, 209.68, 216.98, 220.84, 227.48, 239.07, 235.33, 235.74, 235.93, 238.03, 241.84, 237.30, 240.36, 247.04, 247.10, 245.55, 245.83, 244.87, 244.47, 244.60, 241.53, 236.87, 232.62, 227.65, 227.63, 233.22, 232.47, 232.80, 228.01, 236.00, 237.59, 239.36, 238.26, 229.86, 222.78, 223.66, 223.83, 222.64, 229.98, 228.26, 237.87, 233.28, 234.40, 236.85, 242.70, 242.21, 245.00, 243.36, 243.85
]

X.reverse()

# DAILY PREDICTION 


n=len(X)

'''
R=np.zeros(n-1)

for i in range(n-1):
    R[i]=((X[i+1]-X[i])/X[i])

sum = 0
for i in range(n-1):
    sum=sum+R[i]

drift = sum/(n-1)

sum=0
for i in range(n-1):
    sum=sum+(R[i]-drift)**2

volatility = np.sqrt(sum/(n-1))

print(drift,volatility)



def simulate_gbm(X, mu, sigma, n_steps, n_simulations,T=1):
   
    dt = 1 / n_steps  # Time step

    W = np.random.normal(loc=0,size=(n_steps, n_simulations))

    
    price_factors = np.zeros((n_steps, n_simulations))
    S=np.zeros((n_steps, n_simulations))
    S[0,:]=X[0]

    for i in range(n_steps):
        for j in range(n_simulations):
            price_factors[i,j] = np.exp((mu-0.5*sigma**2)*dt+np.sqrt(dt)*sigma*W[i,j])
    
    
    time_points = np.linspace(0, n_steps, n_steps+1)
    for i in range(n_steps-1):
        S[i+1,:] = X[i] * (price_factors[i+1,:]/price_factors[i,:])
        
              
    
    return time_points, S
    

t, S = simulate_gbm(X, drift, volatility, n , 1)

time = np.linspace(0,1,n)


plt.plot(time, S, 'red')
plt.plot(time, X, 'blue')

difference=np.zeros(n)
values=np.zeros(n)
for i in range(n):
    difference[i] = X[i]-S[i,0] 
    values[i] = np.abs(difference[i])/X[i]

MAPE = np.sum(values[i] for i in range(n))*100/n
print(MAPE)

#plt.plot(time, difference)
plt.ylabel("Stock price ($)")
plt.xlabel("Time (years)")

plt.show()



'''


# YEARLY PREDICTION


n=len(X)


R=np.zeros(n-1)

for i in range(n-1):
    R[i]=((X[i+1]-X[i])/X[i])

sum = 0
for i in range(n-1):
    sum=sum+R[i]

drift = sum/(n-1)

sum=0
for i in range(n-1):
    sum=sum+(R[i]-drift)**2

volatility = np.sqrt(sum/(n-1))

drift = drift*n
volatility = volatility*np.sqrt(n)

print(drift,volatility)



def simulate_gbm(s0, mu, sigma, n_steps, n_simulations,T=1):
   
    dt = 1 / n_steps  # Time step

    W = np.random.normal(loc=0,size=(n_steps, n_simulations))

    
    price_factors = np.zeros((n_steps, n_simulations))
    S=np.zeros((n_steps, n_simulations))
    S[0,:] = s0

    for i in range(n_steps):
        for j in range(n_simulations):
            price_factors[i,j] = np.exp((mu-0.5*sigma**2)*dt+np.sqrt(dt)*sigma*W[i,j])
    
    
    time_points = np.linspace(0, n_steps, n_steps+1)
    for i in range(n_steps-1):
        S[i+1,:] = S[i,:] * price_factors[i,:]
              
    
    return time_points, S
    

time, S = simulate_gbm(X[0], drift, volatility, n , 10)

plt.plot(S, 'pink')
plt.plot(X, 'blue')
plt.ylim(0,500)
plt.ylabel("Stock price ($)")
plt.xlabel("Time (years)")

plt.show()

difference=np.zeros(n)
values=np.zeros(n)
MAPE=np.zeros(10)
for j in range(10):
    for i in range(n):
        difference[i] = X[i]-S[i,j] 
        values[i] = np.abs(difference[i])/X[i]
    MAPE[j]=np.sum(values[k] for k in range(n))*100/n

avg_MAPE = np.sum(MAPE[k] for k in range(10))/10
print(avg_MAPE)

print('n=', n)



    


