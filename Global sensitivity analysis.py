import numpy as np
import copy
import random
import networkx as nx


N = 30  # number of eFAST samples
runs_per_point = 10  # Monte Carlo averaging

# Frequencies
w_n = 1
w_c = 3
w_theta = 5

# Parameter ranges
n_min, n_max = 5, 50
c_min, c_max = 0.5, 1.0
theta_min, theta_max = 0.7, 0.95


def transform(s, w, a, b):
    return 0.5 * ((b + a) + (b - a) * np.sin(w * s))


def run_model(n, c, theta):

    def variations(n, theta, c):

        N = 100
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

           
        t, V_1, Z_1, V_2, Z_2 = simulation(n, 50, theta, c)
    
        f_base = np.sum(Z_1[i] for i in range(n))
        f_shock = np.sum(Z_2[i] for i in range(n))
    
        F_stab = (f_base/n)
        F_cascade = ((f_shock-f_base)/n)
    
        return F_stab, F_cascade

    F_stab, F_cascade = variations (n, theta, c)
    return F_stab, F_cascade


# -----------------------------
# 4. MONTE CARLO AVERAGING
# -----------------------------
def averaged_model(n, c, theta, runs=runs_per_point):
    results_stab = []
    results_cascade = []
    for _ in range(runs):
        a, b = run_model(n, c, theta)
        results_stab.append(a)
        results_cascade.append(b)
    return np.mean(results_stab), np.mean(results_cascade)


s_values = np.linspace(0, 2*np.pi, N)
Y = []
Z = []

for s in s_values:
    # Transform parameters
    n = int(transform(s, w_n, n_min, n_max))
    c = transform(s, w_c, c_min, c_max)
    theta = transform(s, w_theta, theta_min, theta_max)

    # Run model
    output1, output2 = averaged_model(n, c, theta)
    Y.append(output1)
    Z.append(output2)

Y = np.array(Y)
Z = np.array(Z)


Y_fft = np.fft.fft(Y)
power_Y = np.abs(Y_fft)**2
total_variance_Y = np.sum(power_Y)

Z_fft = np.fft.fft(Z)
power_Z = np.abs(Z_fft)**2
total_variance_Z = np.sum(power_Z)


def get_sensitivity(power, total_variance, freq):
    return power[freq] / total_variance

S_n_stab = get_sensitivity(power_Y, total_variance_Y, w_n)
S_c_stab = get_sensitivity(power_Y, total_variance_Y, w_c)
S_theta_stab = get_sensitivity(power_Y, total_variance_Y, w_theta)

S_n_casc = get_sensitivity(power_Z, total_variance_Z, w_n)
S_c_casc = get_sensitivity(power_Z, total_variance_Z, w_c)
S_theta_casc = get_sensitivity(power_Z, total_variance_Z, w_theta)


print("First-order sensitivity indices for stability:")
print(f"n: {S_n_stab:.4f}")
print(f"theta: {S_theta_stab:.4f}")
print(f"c: {S_c_stab:.4f}")

print("First-order sensitivity indices for cascades:")
print(f"n: {S_n_casc:.4f}")
print(f"theta: {S_theta_casc:.4f}")
print(f"c: {S_c_casc:.4f}")
