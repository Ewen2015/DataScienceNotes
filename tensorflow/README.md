# study journal

## study list
1. [Intro to TensorFlow for Deep Learning](https://www.udacity.com/course/intro-to-tensorflow-for-deep-learning--ud187)
2. 

### March, 17, 2020
**[ITTFDL: Lesson 3](https://classroom.udacity.com/courses/ud187/lessons/e52f6e56-2fbc-4ba8-9f74-377937b7da5c/concepts/48e11de0-ccf9-4b2e-81a7-f46c11885583)** 
1. **The Rectified Linear Unit (ReLU)**: As we can see, the ReLU function gives an output of 0 if the input is negative or zero, and if input is positive, then the output will be equal to the input. **ReLU gives the network the ability to solve nonlinear problems.**
2. [Rectified Linear Units (ReLU) in Deep Learning](https://www.kaggle.com/dansbecker/rectified-linear-units-relu-in-deep-learning)
3. **Build, Compile, Train (BCT)**

- **Flattening:** The process of converting a 2d image into 1d vector
- **ReLU:** An activation function that allows a model to solve nonlinear problems
- **Softmax:** A function that provides probabilities for each possible output class
- **Classification:** A machine learning model used for distinguishing among two or more output categories

### March, 16, 2020
**[Reduce Loss](https://developers.google.com/machine-learning/crash-course/reducing-loss/video-lecture)**
1. The gradient descent algorithm then calculates the gradient of the loss curve at the starting point. **The gradient of the loss is equal to the derivative (slope) of the curve**, and tells you which way is "warmer" or "colder." When there are multiple weights, the gradient is a vector of partial derivatives with respect to the weights.
2. Note that a gradient is a vector, so it has both of the following characteristics: **1) a direction 2) a magnitude** 

### March, 14, 2020
**[Intro to TensorFlow for Deep Learning](https://www.udacity.com/course/intro-to-tensorflow-for-deep-learning--ud187)** 
1. Create a model:
    - Build a layer
    - Assemble layers into the model
2. Compile the model, with loss and optimizer functions
3. Train the model

By now you should know what the following terms are:

- Feature: The input(s) to our model
- Examples: An input/output pair used for training
- Labels: The output of the model
- Layer: A collection of nodes connected together within a neural network.
- Model: The representation of your neural network
- Dense and Fully Connected (FC): Each node in one layer is connected to each node in the previous layer.
- Weights and biases: The internal variables of model
- Loss: The discrepancy between the desired output and the actual output
- MSE: Mean squared error, a type of loss function that counts a small number of large discrepancies as worse than a large number of small ones.
- Gradient Descent: An algorithm that changes the internal variables a bit at a time to gradually reduce the loss function.
- Optimizer: A specific implementation of the gradient descent algorithm. (There are many algorithms for this. In this course we will only use the “Adam” Optimizer, which stands for ADAptive with Momentum. It is considered the best-practice optimizer.)
- Learning rate: The “step size” for loss improvement during gradient descent.
- Batch: The set of examples used during training of the neural network
- Epoch: A full pass over the entire training dataset
- Forward pass: The computation of output values from input
- Backward pass (backpropagation): The calculation of internal variable adjustments according to the optimizer algorithm, starting from the output layer and working back through each layer to the input.

