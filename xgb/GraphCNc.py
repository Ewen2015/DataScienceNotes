#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      EwenWangSH@cn.ibm.com
company:    IBM
"""
import warnings
warnings.filterwarnings('ignore')
import time
from datetime import datetime

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import networkx as nx 
import tensorflow as tf 
import sklearn as sk 

def onehot_encoder(labels):
    """独热编码器, 适用于分类目标变量.

    输入:
        labels: 分类目标变量, list. 

    输出:
        labels_onehot: 独热编码后的目标变量, numpy.array.
        classes: 分类类别, list.
    """
    classes = set(labels)
    classes_dict = {c: np.identity(len(classes))[i, :] for i, c in enumerate(classes)}
    labels_onehot = np.array(list(map(classes_dict.get, labels)), dtype=np.int32)
    return labels_onehot, [*classes]

def adjacency_normalizer(adj):
    """邻接矩阵标准化器.

    输入:
        adj: 需要标准化的邻接矩阵, numpy.matrix. 

    输出:
        a_norm: 标准化后的邻接矩阵, numpy.matrix.
    """
    adj = adj + np.eye(adj.shape[0])                        # 增加结点自连接.
    d = np.diagflat(np.power(np.array(adj.sum(1)), -1))     # 计算次数矩阵, degree matrix.
    a_norm = d.dot(adj)                                     # 标准化.
    return a_norm

def graph_convolution(a, x, w, b, name=None):
    """GCN卷积层.

    输入:
        a: 标准化后的邻接矩阵, numpy.matrix. 
        x: 结点特征矩阵, pandas.DataFrame.
        w: 权重, tensorflow.tensor.
        b: 偏差, tensorflow.tensor.
        name: 卷积层名称, str. 

    输出:
        以tensorflow.nn.tanh激活的核函数, tensorflow.tensor.
    """
    with tf.name_scope(name, 'gcn_layer', [a, x, w, b]):    # 规范计算图(computational graph).
        kernel = tf.add(tf.matmul(a, tf.matmul(x, w)), b)   # 核函数.
        return tf.nn.tanh(kernel)                           # 激活核函数, tensorflow.nn.tanh().

class GraphCN(object):
    """GraphCN类, GCN模块化算法库."""
    def __init__(self, edgelist, data, nodecol, target, features, target_multi, multi_label=False, seed=0):
        """GCN类初始化.

        输入:
            edgelist: 边列表, 应包含出发点、目标点两列, pandas.DataFrame.
            data: 数据, 包含点索引、特征变量、目标变量, pandas.DataFrame.
            nodecol: 索引列名称, str.
            target: 目标变量名称, str.
            features: 特征变量名称列表, list.
            target_multi: 多标签目标变量名称列表, list.
            multi_label: 是否进行多标签分类, boolen. 
            seed: 随机种子, int.  
        """
        super(GraphCN, self).__init__()
        self.edgelist = edgelist
        self.data = data 
        self.nodecol = nodecol
        try:
            self.target = target
        except Exception as e:
            self.target = None
        self.features = features
        try:
            self.target_multi = target_multi  
        except Exception as e:
            self.target_multi = None 
        self.multi_label = multi_label
        self.seed = seed
        
        self.g = nx.from_pandas_edgelist(self.edgelist,                             # 由边数据生成图.
                                         source=self.edgelist.columns[0],
                                         target=self.edgelist.columns[1],
                                         create_using=nx.MultiDiGraph())
        self.a = adjacency_normalizer(nx.to_numpy_matrix(self.g))                   # 获得邻接矩阵.

        self.df = pd.DataFrame({self.nodecol: self.g.nodes()})                      # 根据图中的点提取数据.
        self.df = self.df.merge(self.data, how='left', on=self.nodecol)

        self.x = self.df[self.features]                                             # 提取特征矩阵.

        if self.multi_label:                                                        # 提取目标矩阵、类别列表.
            self.y = self.df[self.target_multi]
            self.classes = self.target_multi
        else:
            self.y, self.classes = onehot_encoder(list(self.df[self.target]))

        self.n_nodes = self.g.number_of_nodes()                                     # 计算图中节点数.
        self.n_features = len(self.features)                                        # 计算特征数.
        self.n_classes = len(self.classes)                                          # 计算类别数.

        self.loss_ls = []
        self.prediction = []

    def model(self, learning_rate=0.001):
        """GCN模型, 架构神经网络计算图.

        架构:
            input layer:        feature matrix.
            1st hidden layer:   graph convolutional layer with adjacency matrix.
            2nd hidden layer:   graph convolutional layer with adjacency matrix.
            3rd hidden layer:   fully connected layer with 512 neurons.
            4th hidden layer:   fully connected layer with 256 neurons.
            5th hidden layer:   fully connected layer with 128 neurons.
            6th hidden layer:   fully connected layer with 64 neurons.
            7th hidden layer:   fully connected layer with 16 neurons.
            output layer:       softmax/sigmoid to classes layer.

        输入:
            learning_rate: 学习速率, float.
        
        输出:
            adjacency: 邻接矩阵占位符, tensorflow.tensor.
            feature: 特征矩阵占位符, tensorflow.tensor.
            label: 标签矩阵占位符, tensorflow.tensor.
            output: 输出变量, tensorflow.tensor.
            loss: 损失变量, tensorflow.tensor.
            training_op: 优化训练操作器, tensorflow.ops.
        """
        tf.reset_default_graph()
        tf.set_random_seed(self.seed)

        n_dense1 = 512          # 设定全连接层各层神经元数量.
        n_dense2 = 256
        n_dense3 = 128
        n_dense4 = 64
        n_dense5 = 16

        adjacency = tf.placeholder(dtype=tf.float32, shape=(self.n_nodes, self.n_nodes))
        feature = tf.placeholder(dtype=tf.float32, shape=(self.n_nodes, self.n_features))
        label = tf.placeholder(dtype=tf.float32, shape=(self.n_nodes, self.n_classes))

        with tf.name_scope('gcn1'):                                                                                         # 第一隐藏层, 图卷积层.
            weight1 = tf.get_variable(initializer=tf.random_normal([self.n_features, self.n_features]), name='weight1')
            bias1 = tf.get_variable(initializer=tf.random_normal([self.n_nodes, self.n_features]), name='bias1')
            gcn1 = graph_convolution(a=adjacency, x=feature, w=weight1, b=bias1, name='gcn_layer1')
        
        with tf.name_scope('gcn1'):                                                                                         # 第二隐藏层, 图卷积层.
            weight2 = tf.get_variable(initializer=tf.random_normal([self.n_features, n_dense1]), name='weight2')
            bias2 = tf.get_variable(initializer=tf.random_normal([self.n_nodes, n_dense1]), name='bias2')
            gcn2 = graph_convolution(a=adjacency, x=gcn1, w=weight2, b=bias2, name='gcn_layer2')

        with tf.contrib.framework.arg_scope([tf.contrib.layers.fully_connected], 
                                            activation_fn=tf.nn.relu):
            dense1 = tf.contrib.layers.fully_connected(inputs=gcn2, num_outputs=n_dense2, scope='dense1')                   # 第三隐藏层, 全连接层, 512个神经元.
            dense2 = tf.contrib.layers.fully_connected(inputs=dense1, num_outputs=n_dense3, scope='dense2')                 # 第四隐藏层, 全连接层, 256个神经元.
            dense3 = tf.contrib.layers.fully_connected(inputs=dense2, num_outputs=n_dense4, scope='dense3')                 # 第五隐藏层, 全连接层, 128个神经元.
            dense4 = tf.contrib.layers.fully_connected(inputs=dense3, num_outputs=n_dense5, scope='dense4')                 # 第六隐藏层, 全连接层, 64个神经元.
            dense5 = tf.contrib.layers.fully_connected(inputs=dense4, num_outputs=self.n_classes, scope='dense5')           # 第七隐藏层, 全连接层, 16个神经元.

        with tf.name_scope('output'):                                                                                       # 输出层.
            if self.multi_label:                                                          # 多标签分类输出层.
                output = tf.nn.sigmoid(x=dense5, name='output')                     
            else:                                                                         # 多分类输出层.
                output = tf.nn.softmax(logits=dense5, axis=-1, name='output')

        with tf.name_scope('loss'):                                                                                         # 损失计量.
            if self.multi_label:
                loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=label))
            else:
                loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=output, labels=label))

        training_op = tf.train.AdamOptimizer(learning_rate).minimize(loss)                                                  # 最优化, Adam最优化.
        return adjacency, feature, label, output, loss, training_op

    def train(self, learning_rate=0.001, n_epochs=3000, verbose=100, early_stopping=10, path_model=None):
        """模型训练器.

        输入:
            learning_rate: learning_rate: 学习速率, float.
            n_epochs: 训练回合, int.
            verbose: 训练结果展示间隔, int.
            early_stopping: 提前停止数, int.
            path_model: 模型保存地址, str.
        
        """
        adjacency, feature, label, output, loss, training_op = self.model(learning_rate)

        init = tf.global_variables_initializer()

        self.best_loss = 9999
        stopping_step = 0

        with tf.Session() as sess:
            sess.run(init)
            for epoch in range(1, n_epochs+1):                                                                          # 回合循环训练
                start_time = time.time()
                training_op.run(feed_dict={adjacency: self.a, feature: self.x, label: self.y})
                cost = loss.eval(feed_dict={adjacency: self.a, feature: self.x, label: self.y})
                self.loss_ls.append(cost)

                if verbose <= 0:                                                                                        # 结果间隔展示
                    pass 
                elif epoch % verbose == 0:
                    duration = time.time() - start_time
                    message = '%s: epoch: %d \tloss: %.6f \tduration: %.2f s' % (datetime.now(), epoch, cost, duration)
                    print(message)

                if self.best_loss > cost:                                                                               # 提前停止机制
                    stopping_step = 0
                    self.best_loss = cost
                else:
                    stopping_step += 1
                    if stopping_step >= early_stopping:
                        print('early stopping triggered at epoch: %d with best loss: %.6f.' % (epoch, cost))
                        break

            self.prediction = pd.DataFrame(output.eval(feed_dict={adjacency: self.a, feature: self.x}), columns=self.classes)

            if path_model == None:                                                                                      # 模型保存
                pass
            else:
                save_path = tf.train.Saver().save(sess, path_model)
                print('model saved in path: %s' % save_path)
        return None

    def evaluate(self, path_model):
        """模型评价器.

        输入:
            path_model: 待评价模型保存地址, str.

        输出:
            多标签分类:
                evaluate_loss: 分类损失, float.
            多分类:
                evaluate_loss: 分类损失, float.
                evaluate_auc: 分类器AUC ROC, float.
                evaluate_ap: 分类器PR ROC, float.
        
        """
        tf.reset_default_graph()
        adjacency, feature, label, output, loss, training_op = self.model()                # 加载计算图
        self.evaluate_loss = None

        saver = tf.train.Saver()

        with tf.Session() as sess:
            saver.restore(sess, path_model)                                                 # 加载模型
            message = 'model loaded from path: %s' % path_model
            print(message)
            self.prediction = pd.DataFrame(output.eval(feed_dict={adjacency: self.a, feature: self.x}), columns=self.classes)
            message = 'prediction done.'
            print(message)

            if self.multi_label:                                                            # 多标签分类评价
                return self.evaluate_loss
            else:                                                                           # 多分类评价
                predprob = self.prediction[self.prediction.columns[1]]
                self.evaluate_auc = sk.metrics.roc_auc_score(self.df[self.target], predprob)
                self.evaluate_pr = sk.metrics.average_precision_score(self.df[self.target], predprob)

                message = '\nevaluation:'+\
                          '\n\tloss: %.6f' % self.evaluate_loss+\
                          '\n\tauc: %.6f' % self.evaluate_auc+\
                          '\n\tpr: %.6f' % self.evaluate_pr
                print(message)
                return self.evaluate_loss, self.evaluate_auc, self.evaluate_pr       

    def predict(self, path_model=None, path_result=None):
        """模型预测器.

        输入:
            path_model: 模型保存地址, str.
            path_result: 预测结果保存地址, str.

        输出:
            prediction: 预测结果, pandas.DataFrame.
        
        """
        tf.reset_default_graph()
        adjacency, feature, label, output, loss, training_op = self.model()                 # 加载计算图

        saver = tf.train.Saver()

        with tf.Session() as sess:
            saver.restore(sess, path_model)                                                 # 加载模型
            message = 'model loaded from path: %s' % path_model
            print(message)
            self.prediction = pd.DataFrame(output.eval(feed_dict={adjacency: self.a, feature: self.x}), columns=self.classes)   # 模型预测
            message = 'prediction done.'
            print(message)

        if path_result == None:
            pass
        else:
            self.prediction.to_csv(path_result, index=False)                                # 保存预测结果
            message = 'results saved in path: %s' % path_result
            print(message)
        return self.prediction

    def retrain(self, learning_rate=0.001, n_epochs=100, verbose=1, early_stopping=10, path_model=None, path_model_update=None):
        """模型持续训练器.

        输入:
            learning_rate: learning_rate: 学习速率, float.
            n_epochs: 训练回合, int.
            verbose: 训练结果展示间隔, int.
            early_stopping: 提前停止数, int.
            path_model: 初始模型保存地址, str.
            path_model_update: 更新模型保存地址, str.
        
        """
        tf.reset_default_graph()
        adjacency, feature, label, output, loss, training_op = self.model(learning_rate)    # 加载计算图

        saver = tf.train.Saver()

        self.best_loss = 9999
        stopping_step = 0

        with tf.Session() as sess:
            saver.restore(sess, path_model)                                                 # 加载模型
            message = 'model loaded from path: %s' % path_model
            print(message)
            for epoch in range(n_epochs):                                                                          # 回合循环训练
                start_time = time.time()
                training_op.run(feed_dict={adjacency: self.a, feature: self.x, label: self.y})
                cost = loss.eval(feed_dict={adjacency: self.a, feature: self.x, label: self.y})
                self.loss_ls.append(cost)

                if verbose <= 0:                                                                                   # 结果间隔展示
                    pass 
                elif epoch % verbose == 0:
                    duration = time.time() - start_time
                    message = '%s: epoch: %d \tloss: %.6f \tduration: %.2f s' % (datetime.now(), epoch, cost, duration)
                    print(message)

                if self.best_loss > cost:                                                                           # 提前停止机制
                    stopping_step = 0
                    self.best_loss = cost
                else:
                    stopping_step += 1
                    if stopping_step >= early_stopping:
                        print('early stopping triggered at epoch: %d with best loss: %.6f.' % (epoch, cost))
                        break

            self.prediction = pd.DataFrame(output.eval(feed_dict={adjacency: self.a, feature: self.x}), columns=self.classes)

            if path_model_update == None:                                                                            # 模型保存
                pass
            else:
                save_path = saver.save(sess, path_model_update)
                print('model saved in path: %s' % save_path)
        return None

    def learning_curve(self):
        """学习曲线, 模型训练后提供学习曲线.
        """
        if len(self.loss_ls) == 0:
            return 'no models trained, no learning curves.'

        self.loss_min, self.loss_max, self.loss_std, self.loss_avg = np.min(self.loss_ls), np.max(self.loss_ls), np.std(self.loss_ls), np.average(self.loss_ls)

        plt.figure(figsize=(10, 4))                                                 # 绘制学习曲线
        plt.plot(self.loss_ls)
        plt.title('learning curve')
        plt.xlabel('number of epochs')
        plt.ylabel('loss')
        plt.ylim(self.loss_min-self.loss_std, self.loss_max+self.loss_std)
        plt.grid() 
        plt.show()

        summary = 'summary:\n'+\
                  'average loss: %.6f (std: %.6f)' % (self.loss_avg, self.loss_std)
        print(summary)                                                              # 展示学习平均损失计量
        return None   

    def report(self):
        """模型汇报器, 在模型训练后提供可视化模型评价.
        """
        try:
            from gossipcat.Report import Visual
        except Exception as e:
            print('[WARNING] Package GossipCat not installed.')
            try:
                from Report import Visual
            except Exception as e:
                return '[ERROR] Package Report not installed.'
        columns = self.prediction.columns

        for ind, val in enumerate(columns):
            if self.multi_label:                                        # 多标签分类中, 针对每一个标签汇报
                print(ind, val)
                test_target=self.df[val]
            else:
                test_target=self.df[self.target]
                if ind == 0:
                    continue
            prob = self.prediction[val]

            plt.figure(figsize=(6, 5.5))                                # 预测分布图
            self.prediction[val].hist(bins=100)
            plt.title('distribution of predictions')

            vis = Visual(test_target=test_target, test_predprob=prob)
            vis.CM()                                                    # 混淆矩阵
            vis.ROC()                                                   # ROC曲线
            vis.PR()                                                    # PR曲线
        return None
