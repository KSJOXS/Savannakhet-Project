# AI Recommendation Demo (GNN)

This folder contains a standalone demonstration of the **Graph Neural Network (GNN)** used in the Savannakhet Project. It is designed to explain the core AI logic to teachers and reviewers.

## Files
- `demo_gnn.py`: The main script that simulates graph creation, training, and recommendation.

## How to Run
1. Open your terminal in the `backend` folder.
2. Execute the following command:
   ```powershell
   ..\.venv\Scripts\python.exe ai_demo/demo_gnn.py
   ```

## Key Concepts for Presentation
1. **Heterogeneous Graph:** We represent Users and Places as different types of "Nodes". Their interactions are "Edges".
2. **Feature Learning:** Initial preferences (Nature/Culture) are converted into numerical vectors.
3. **GraphSAGE (SAGEConv):** The AI learns by "aggregating" information from neighbors. A user node becomes similar to the places they visit.
4. **Link Prediction:** The model is trained to predict future links between users and places using Binary Cross Entropy loss.
5. **Embedding Space:** After training, the AI maps users and places into a multi-dimensional space where "similar" items are closer together, enabling personalized recommendations.
