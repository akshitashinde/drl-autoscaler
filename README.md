# Intelligent Auto-Scaling of Cloud Workloads Using Deep Reinforcement Learning

**Team Members:**  
- Ronit Chandresh Virwani  
- Sanket Rajesh Nagarkar  
- Akshita Ashwin Shinde  

---

## Table of Contents

1. [Introduction & Motivation](#introduction--motivation)  
2. [Core Concepts](#core-concepts)  
3. [Key Components](#key-components)  
4. [How It Works – Step by Step](#how-it-works--step-by-step)  
5. [Installation & Quickstart](#installation--quickstart)  
6. [Results & Evaluation](#results--evaluation)   

---

## Introduction & Motivation

Cloud providers charge based on the number of containers or virtual machines running. Traditional auto-scalers use fixed rules (e.g., “add one pod if CPU > 70% for 2 minutes”), which can lead to:

- **Over-Provisioning:** Wasting money on idle servers.  
- **Under-Provisioning:** Slow performance during traffic spikes.  

**Goal:** Build a **self-learning auto-scaler** that continuously adjusts replicas to minimize cost and maintain performance—no manual threshold tuning required :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}.

---

## Core Concepts

### 1. Reinforcement Learning (RL)  
- **Agent:** The auto-scaler decision-maker  
- **Environment:** Cloud workload (simulated or real)  
- **State:** Metrics like CPU %, memory %, request rate, pod count  
- **Action:** Discrete choices: scale down, hold, scale up  
- **Reward:** Numeric score balancing cost savings and SLA adherence :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}  

### 2. Deep Q-Network (DQN)  
- **Q-Value:** Expected cumulative reward for action *a* in state *s*  
- **Neural Network:** Approximates Q(s, a) for all actions  
- **Experience Replay:** Stabilizes learning by reusing past transitions  
- **Target Network:** A delayed copy of the main network to improve convergence :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}  

### 3. Kubernetes Horizontal Pod Autoscaler (HPA)  
- Built-in resource that adjusts pod replicas based on metric thresholds.  
- Our custom operator patches HPA’s `targetCPUUtilizationPercentage` and `maxReplicas` based on DRL recommendations :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}.

---

## Key Components

1. **Simulation Environment** (`simulation.py`, `scaling_env.py`)  
   - Generates synthetic CPU load and cost for fast, risk-free training.  

2. **DRL Agent** (`train_agent.py`)  
   - Trains a DQN on the simulated environment (100 k+ steps) → outputs `drl_scaling_model.zip`.  

3. **Prediction Service** (`app.py`)  
   - Flask API exposing `/predict`; loads the trained model and maps actions to HPA settings.  

4. **Kubernetes Operator** (`scaling_operator.py`)  
   - Kopf-based controller in the cluster; polls `/predict` → patches HPA via the Kubernetes API.  

5. **Data & Monitoring**  
   - **Cloud Monitoring:** Real-time collection of CPU, memory, latency, request rate.  
   - **BigQuery:** Historical metrics storage via a Logging sink; used for retraining and analysis.  
   - **Grafana/Data Studio:** Dashboards for cost, performance, and scaling events.  

6. **CI/CD & Deployment**  
   - Docker images for agent and operator.  
   - Automated build and deploy using GitHub Actions or Cloud Build.

---

## How It Works – Step by Step

1. **Offline Training**  
   - Run `train_agent.py` in the simulated environment.  
   - Model learns optimal scaling policy over 100 k timesteps.  
   - Saved as `drl_scaling_model.zip`.  

2. **Prediction Service Deployment**  
   - Containerize `app.py` with the trained model.  
   - Expose `/predict` endpoint in GKE.  

3. **Control Loop**  
   - Operator polls `/predict` every 30 s.  
   - Receives `{ replica_count, target_cpu }` → patches HPA in the cluster.  
   - HPA adjusts pod replicas accordingly.  

4. **Data Feedback**  
   - Live metrics funnel into Cloud Monitoring.  
   - Logs sink into BigQuery for future retraining.  

---

## Installation & Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/your-org/smart-cloud-helper.git
cd smart-cloud-helper

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Train the model
python train_agent.py

# 5. Run a dummy demo to show output
python dummy_demo.py

# 6. Launch the prediction service
python app.py

# 7. In another terminal, run the operator locally
kopf run scaling_operator.py --namespace default

## Results & Evaluation

- **Simulation Results**: ~20 % cost reduction vs. static HPA thresholds, with stable response times.

- **Operator Overhead**: < 1 % CPU on the control plane.

- **Resilience**: Falls back to default HPA settings if the RL service is unavailable 



