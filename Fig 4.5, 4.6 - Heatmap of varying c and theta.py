import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import copy


def variations(n, theta, c):

    N = 10
    def simulation(n, T, theta, c):

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

        

        time, paths = simulate_gbm(initial_price, expected_return, standard_deviation, T, n)
        p_1 = copy.deepcopy(paths)
        p_2 = copy.deepcopy(paths)
    

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

        C = generating_C(n,c)


        def equity_value(p, C, beta):
            I = np.eye(n)
            IC_inv = np.linalg.inv(I-C)
            A = 0.7*p
            D = np.matmul(beta, C)
            V = np.matmul(IC_inv, A - D)

            return V



        #3. THE ALGORITHM

        def algorithm_1(p_1, C, theta):

            p=p_1
            B = np.zeros(n)
            V_0 = equity_value(p[0], C, B)
    
            # calculate the failure thresholds

            v_failure = theta*V_0

            t = np.linspace(0,T-1,T)
        
            Z=np.zeros((n))
            V=np.ones((T,n))
            V[0]=V_0
    
            for i in range(T-1):
                v_new = equity_value(p[i], C, B)
            
    
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
        


            return t, V, Z


        def algorithm_2(p_2, C, theta):
            p=p_2
            B = np.zeros(n)
        
            V_0 = equity_value(p[0], C, B)
    
            # calculate the failure thresholds

            v_failure = theta*V_0

            p[1:,random_company]=0
            B[random_company]=V_0[random_company]
    
            t = np.linspace(0,T-1,T)
        
            Z=np.zeros((n))
            V=np.ones((T,n))
            V[0]=V_0

        
    
            for i in range(T-1):
                v_new = equity_value(p[i], C, B)
            
    
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
        


            return t, V, Z
    
        t, V_1, Z_1 = algorithm_1(p_1, C, theta)
        t, V_2, Z_2 = algorithm_2(p_2, C, theta)

        return t, V_1, Z_1, V_2, Z_2



    F_stab = []
    F_cascade = []
    
    for i in range(N):
        t, V_1, Z_1, V_2, Z_2 = simulation(n, 50, theta, c)

        f_base = np.sum(Z_1[i] for i in range(n))
        f_shock = np.sum(Z_2[i] for i in range(n))

        F_stab.append(f_base/n)
        F_cascade.append((f_shock)/n)

    return F_stab, F_cascade



t = np.linspace(0.1,1.1,10)
mean_F_stab = []
std_F_stab = []
mean_F_cascade = []
std_F_cascade = []


def data_analysis(data_points):
    mean_f = np.mean(data_points)
    std_f = np.std(data_points)

    return mean_f, std_f


c_values = np.linspace(0, 1.0, 25)
theta_values = np.linspace(0.7, 0.99, 25)

Z_stability = np.zeros((len(theta_values), len(c_values)))
Z_cascade = np.zeros((len(theta_values), len(c_values)))
for i in range(len(theta_values)):
    for j in range(len(c_values)):

        F_stab, F_cascade = variations(30, theta_values[i], c_values[j])
        mu_F_stab, sigma_F_stab = data_analysis(F_stab)
        mu_F_cascade, sigma_F_cascade = data_analysis(F_cascade)
        Z_stability[i, j] = mu_F_stab
        Z_cascade[i, j] = mu_F_cascade


plt.figure()
plt.pcolormesh(c_values, theta_values, Z_cascade)

plt.colorbar(label='Cascade measure ($F_{shocks}$)')



plt.xlabel('Maximum Ownership Percentage (c)')
plt.ylabel('Failure Threshold Percentage')
plt.title('Sensitivity Heatmap')

plt.show()
