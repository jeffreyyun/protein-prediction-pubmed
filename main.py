import tensorflow as tf
import numpy as np
import scipy.io as io
from matplotlib import pyplot as plt
from parameters import *
import re
import random

# Global variables.
BATCH_SIZE = 10  # The number of training examples to use per training step.
# Define the flags useable from the command line.
tf.app.flags.DEFINE_string('train', None,
                           'File containing the training data (labels & features).')
tf.app.flags.DEFINE_integer('num_epochs', 1,
                            'Number of training epochs.')
tf.app.flags.DEFINE_boolean('verbose', False, 'Produce verbose output.')
FLAGS = tf.app.flags.FLAGS
anchors_file="anchors.txt"
nonanchors_file="nonanchors.txt"

# Extract numpy representations of the labels and features given rows consisting of:
#   label, feat_0, feat_1, ..., feat_n
#   The given file should be a comma-separated-values (CSV) file saved by the savetxt command.
def extract_data():
    global anchors_file
    file_object  = open(anchors_file, 'r')
    anchors_array=[]
    for line in file_object:
        #remove extra spaces
        line=re.sub(' +',' ',line)
        seq=line.split(' ')[1][:-1]
        anchors_array.append([seq,1])
    file_object  = open(nonanchors_file, 'r')
    nonanchors_array=[]
    for line in file_object:
        #remove extra spaces
        line=re.sub(' +',' ',line)
        seq=line.split(' ')[1][:-1]
        nonanchors_array.append([seq,0])

    training= ( anchors_array[0:len(anchors_array)*8//10] +
        nonanchors_array[0:len(nonanchors_array)*8//10] )
    validation= ( anchors_array[len(anchors_array)*8//10:len(anchors_array)*9//10] +
        nonanchors_array[len(nonanchors_array)*8//10: len(nonanchors_array)*8//10] )
    test= ( anchors_array[len(anchors_array)*9//10:] +
        nonanchors_array[len(nonanchors_array)*9//10:] )
    random.shuffle(training)
    random.shuffle(validation)
    random.shuffle(test)
    return (training, validation,test)



def main(argv=None):
    # Be verbose?
    verbose = FLAGS.verbose

    # Plot?
    plot = FLAGS.plot

    # Get the data.
    train_data_filename = FLAGS.train

    # Extract it into numpy matrices.
    training,validation, test = extract_data(train_data_filename)
    train_data,train_labels =

    # Convert labels to +1,-1
    train_labels[train_labels==0] = -1

    # Get the shape of the training data.
    train_size,num_features = train_data.shape

    # Get the number of epochs for training.
    num_epochs = FLAGS.num_epochs

    # Get the C param of SVM
    svmC = FLAGS.svmC

    # This is where training samples and labels are fed to the graph.
    # These placeholder nodes will be fed a batch of training data at each
    # training step using the {feed_dict} argument to the Run() call below.
    x = tf.placeholder("float", shape=[None, num_features])
    y = tf.placeholder("float", shape=[None,1])

    # Define and initialize the network.

    # These are the weights that inform how much each feature contributes to
    # the classification.
    W = tf.Variable(tf.zeros([num_features,1]))
    b = tf.Variable(tf.zeros([1]))
    y_raw = tf.matmul(x,W) + b

    # Optimization.
    regularization_loss = 0.5*tf.reduce_sum(tf.square(W))
    hinge_loss = tf.reduce_sum(tf.maximum(tf.zeros([BATCH_SIZE,1]),
        1 - y*y_raw));
    svm_loss = regularization_loss + svmC*hinge_loss;
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(svm_loss)

    # Evaluation.
    predicted_class = tf.sign(y_raw);
    correct_prediction = tf.equal(y,predicted_class)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    # Create a local session to run this computation.
    with tf.Session() as s:
        # Run all the initializers to prepare the trainable parameters.
        tf.initialize_all_variables().run()
        if verbose:
            print('Initialized!')
            print()
            print('Training.')

        # Iterate and train.
        for step in range(num_epochs * train_size // BATCH_SIZE):
            if verbose:
                print(step, end=' ')

            offset = (step * BATCH_SIZE) % train_size
            batch_data = train_data[offset:(offset + BATCH_SIZE), :]
            batch_labels = train_labels[offset:(offset + BATCH_SIZE)]
            train_step.run(feed_dict={x: batch_data, y: batch_labels})
            print('loss: ', svm_loss.eval(feed_dict={x: batch_data, y: batch_labels}))

            if verbose and offset >= train_size-BATCH_SIZE:
                print()

        # Give very detailed output.
        if verbose:
            print()
            print('Weight matrix.')
            print(s.run(W))
            print()
            print('Bias vector.')
            print(s.run(b))
            print()
            print("Applying model to first test instance.")
            print()

        print("Accuracy on train:", accuracy.eval(feed_dict={x: train_data, y: train_labels}))

        if plot:
            eval_fun = lambda X: predicted_class.eval(feed_dict={x:X});
            plot_boundary_on_data.plot(train_data, train_labels, eval_fun)

if __name__ == '__main__':
    tf.app.run()