# A0: Build a Linear Regression model

## Summary
This project implements **Linear Regression**, **Ridge Regression**, and **LASSO Regression** using Python. The main goal was to understand the process of building a basic ML model. We broke down the process of implementing Linear Regression in Python using a simple dataset known as **Boston Housing**, step by step.

The notebook includes:
- Data preprocessing and normalization  
- Manual implementation of cost and gradient functions  
- Batch Gradient Descent  
- Ridge (L2) and LASSO (L1) regularization  
- Model evaluation using Mean Squared Error (MSE)  
- Visual interpretation of feature importance  

---

## Collaboration
- **Daniel Tseng**  
- **Chia-En Wu**

During this assignment, I discussed the math equations and implementation details with **Daniel Tseng** and **Chia-En Wu**.  
We helped each other understand the formulas and debug whenever we got stuck or came up with some crazy answers.

---

## Reflections

### What Was Easy
- Loading and splitting the dataset  
- Writing the visualization parts (cost curve, scatter plot, and bar chart)  
- Understanding the effect of normalization and regularization intuitively  

### What Was Hard
- Deriving the **gradients** for weight and bias from the cost function —  
  I struggled to fully understand how the mathematical formula translates into code,  
  especially when updating `w` and `b` during gradient descent. Also, my gradient descent didn’t converge correctly because of a misunderstanding in the **partial derivatives**.  
  It took several print checks and visual plots to confirm the updates were working as expected.  

---

## Resources Used
- Class materials and lecture notes  
- ChatGPT (for debugging and conceptual clarification)

---
