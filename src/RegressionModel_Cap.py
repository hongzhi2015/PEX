"""
Author: Geraldo Pradipta

BSD 3-Clause License

Copyright (c) 2019, The Regents of the University of Minnesota

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
© 2019 GitHub, Inc.
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np 
import tensorflow as tf
import matplotlib.pyplot as plt
import glob
import os
import time
import re

def run_regression(layer, dataset, cap_storage):
    """ Train the data
    
    Train the regression model with data generated by Innovus using tensor
    flow library.
    
    Args:
        layer: an int representing current metal layer 
        dataset: a list that contains the training data
        cap_storage: a list that stores the regression data
        
    Returns:
        cap_storage -> the list is filled with the trained data
            - The data is in form of [capacitance = a*X + b], X is length of wire
            - Trained data are {a} and {b}
    """
    
    start_point = SAMPLE_CAP*layer - SAMPLE_CAP
    end_point = SAMPLE_CAP*layer
    
    data_cap = dataset[start_point:end_point,[0,1]]

    X = tf.placeholder(tf.float32, name="X")
    Y = tf.placeholder(tf.float32, name="Y")

    w = tf.Variable(0.0, name="weights")
    b = tf.Variable(0.0, name="bias")

    Y_predicted = X * w + b

    cost = tf.reduce_sum(tf.pow(Y_predicted-Y, 2))/(2*SAMPLE_CAP)

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.08).minimize(cost)
    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        print('\n#  Training Data: Metal Layer ' + str(layer))
        prev_loss = 0
        counter = 0
        for i in range(EPOCHS):

            progbar(i,EPOCHS-1,30)
            for x, y in data_cap:
                _,loss_v = sess.run([optimizer,cost], feed_dict={X: x, Y:y})
    		
            w_value, b_value = sess.run([w, b])
            if loss_v != prev_loss:
                prev_loss = loss_v
            else:
                counter += 1
            
            # If the loss has coverged
            if counter == 20:
                progbar(EPOCHS-1,EPOCHS-1,30)
                break
    
        cap_storage.append([layer, w_value, b_value])
    
# Display progressBar during training
def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')
          
def write_toFile(arr, filename, cap_storage):
    with open('./output/' + filename + '.txt','a') as out:
        out.write('\nCAPACITANCE\n')
        out.write('Layer W b\n')
        
        for ele in cap_storage:
            out.write(str(ele[0]) + ' ' + str(ele[1]) + ' ' + str(ele[2]) + '\n')
            
        out.write('END\n')

def get_corner_type(file):
    with open(file) as f:
        first_line = f.readline()
        corner_type = re.match('Corner Type: (\w+)',first_line, flags=re.IGNORECASE).group(1)
        
    return corner_type
        
def main():
    # IO file name
    filename = 'config_file'
    in_file = './work/Cap_TrainingSet_*.txt'
    
    # Translate data into an array
    for file in glob.glob(in_file):
        assert os.path.exists(file), '{} file does not exist'.format(file)
        start_time = time.time()
        dataset=np.genfromtxt(file, delimiter=" ", skip_header=2) #reads file
        
        # Get corner type 
        corner_type = get_corner_type(file)
        
        print('\n# Start Training Regression Model for: {}'.format(corner_type))
              
        # Compute the # of layers
        total_layer = int(len(dataset)/SAMPLE_CAP)
        
        cap_storage = []
        for metal_layer in range (1, total_layer+1):
            run_regression(metal_layer, dataset, cap_storage)
        
        outFile = filename + '_' + corner_type
        
        # Writing the data to the config file    
        write_toFile(cap_storage, outFile, cap_storage)
    
    print('\n# Completed - Total Elapsed Time: {} seconds'.format(time.time() - start_time))


##############################################
# Global Variables Initialiazation 
##############################################
EPOCHS = 800
SAMPLE_CAP = 199

main()