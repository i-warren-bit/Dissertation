import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import networkx as nx


def simulation(n, T):

    #1. BROWNIAN MOTION
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
    

    #2. INITIALISING VARIABLES
    initial_price = 1  # Initial stock price
    expected_return = 0.1171 # Annual expected return (10%)
    standard_deviation = 0.15 


    #failure threshold
    alpha = 1 #ratio of external assets to stock prices
    outstanding_shares = (2.319, 5.048, 3.368, 4.003, 2.550, 30.767)
    


    time, paths = simulate_gbm(initial_price, expected_return, standard_deviation, T, n)
    p_1 = copy.deepcopy(paths)
    p_2 = copy.deepcopy(paths)

    theta = 0.9
    
    
    

    random_company = random.randint(0,n-1) #setting a random company to fail
    

    def generating_C(n,c):
        n_nodes = n
        G = nx.DiGraph(nx.scale_free_graph(n_nodes))
        G.remove_edges_from(nx.selfloop_edges(G))

        G_matrix = nx.to_numpy_array(G)
    
        d = []
        for j in range(n):
            d.append(np.sum(G_matrix[i,j] for i in range(n)))

        C=np.zeros([n,n])
        for i in range(n):
            for j in range(n):
                C[i,j]=c*G_matrix[i,j]/d[j]
                if d[j]==0:
                    C[i,j]=0

        return C

    #C = generating_C(n,0.5)
    C = [
    [0.000, 0.008, 0.010, 0.052, 0.001, 0.135],
    [0.040, 0.000, 0.080, 0.049, 0.059, 0.031],
    [0.056, 0.084, 0.000, 0.075, 0.214, 0.052],
    [0.044, 0.061, 0.137, 0.000, 0.013, 0.112],
    [0.004, 0.071, 0.041, 0.011, 0.000, 0.004],
    [0.189, 0.110, 0.065, 0.147, 0.047, 0.000]
]


    def equity_value(outstanding_shares, p, alpha, C, beta):
        I = np.eye(n)
        IC_inv = np.linalg.inv(I-C)
        market_cap=np.zeros(n)
        for i in range(n):
            market_cap[i] = outstanding_shares[i]*p[i]
        A = market_cap*alpha
        D = np.matmul(beta, C)
    
        V = np.matmul(IC_inv, A - D)

        return V



    #3. THE ALGORITHM

    def algorithm_1(outstanding_shares, p_1, alpha, C, theta):

        p=p_1
        B = np.zeros(n)
        V_0 = equity_value(outstanding_shares, p[0], alpha, C, B)
        print(V_0)
    
        # calculate the failure thresholds

        #v_failure = alpha*np.multiply(outstanding_shares, p_1[0])
        v_failure = theta*V_0
        print(v_failure)

        t = np.linspace(0,T-1,T)
        
        Z=np.zeros((n))
        V=np.ones((T,n))
        V[0]=V_0
    
        for i in range(T-1):
            v_new = equity_value(outstanding_shares, p[i], alpha, C, B)
            
    
            for j in range(n):
                if Z[j]==1:
                    v_new[j]=0
                
    
            for j in range(n):
                if v_new[j]<v_failure[j]:           
                    p[:,j]=0
                    Z[j]=1
                    B[j]=V[i,j]
                    v_new[j]=0 
                
           
            V[i+1]=(v_new)
        


        return t, V


   
    t, V = algorithm_1(outstanding_shares, p_1, alpha, C, theta)
    

    return t, V

n=6

t, V = simulation(n, 50)



plt.rcParams.update({'font.size': 9})

plt.plot(t,V, label=['Canada', 'Germany', 'France', 'UK', 'Italy', 'US' ])
plt.xlabel('Time, t')
plt.ylabel('Equity Value')

plt.legend()
plt.show()

