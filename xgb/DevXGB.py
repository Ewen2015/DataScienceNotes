#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      EwenWangSH@cn.ibm.com
company: 	IBM
"""
import warnings
warnings.filterwarnings('ignore')
import random
random.seed(0)

import time
import json
import pickle

import pandas as pd 
import matplotlib.pyplot as plt 
import xgboost as xgb 

class DevXGB(object):
    """docstring for DevXGB"""
    def __init__(self, data, indcol, target, features, training=1, multi=0, balanced=1, gpu=0, seed=0):
        """DevXGB类初始化.

        输入:
            data: 数据, 包含点索引、特征变量、目标变量, pandas.DataFrame.
            indcol: 索引列名称, str.
            target: 目标变量名称, str.
            features: 特征变量名称列表, list.
            training: 是否用于训练模型, 0/1, 默认1.
            multi: 是否为多分类任务, 0/1, 默认0.
            balanced: 样本是否平衡, 0/1, 默认1.
            gpu: 是否运用GPU，, 0/1, 默认0.
            seed: 随机种子, int.  
        """
        super(DevXGB, self).__init__()
        self.data = data
        self.indcol = indcol
        self.features = features
        self.training = training

        if self.training:                                                       # 生成XGBoost格式数据
            self.target = target
            self.dtrain = xgb.DMatrix(self.data[self.features], label=self.data[self.target])
        else:
            self.target = None
            self.dtest = xgb.DMatrix(self.data[self.features])
        
        self.multi = multi
        self.balanced = balanced
        self.gpu = gpu
        self.seed = seed

        self.cvr = pd.DataFrame()
        self.prediction = pd.DataFrame()
    
    def algorithm(self, learning_rate=0.01, n_rounds=3000, early_stopping=20, verbose=100):
        """设置算法(gradient boosting machine)的超参数(hpyer-parameters). 其中 n_rounds 通过交叉验证(cross-validation) 进行更新，防止过拟合.

        输入:
            learning_rate: learning_rate: 学习速率, float.
            n_rounds: 训练回合, int.
            early_stopping: 提前停止数, int.
            verbose: 训练结果展示间隔, int.
        """
        self.learning_rate = learning_rate
        self.n_rounds = n_rounds
        self.early_stopping = early_stopping
        self.verbose = verbose

        start_time = time.time()
        message = 'cross validation started and will stop if performace did not improve in %d rounds.' % self.early_stopping
        print(message)
        self.params = {
            'objective': 'binary:logistic',
            'tree_method': 'hist',
            'eval_metric': 'auc',
            'eta': self.learning_rate,
            'max_depth': 3,
            'subsample': 0.75,
            'colsample_bytree': 0.75,
        }                                                                       # 设定参数
        if self.balanced == 0:                                                  # 根据样本平衡性，设定评价指标
            self.params['eval_metric'] = 'aucpr'
        if self.gpu == 1:                                                       # 根据计算硬件，设置GPU参数
            self.params['tree_method'] = 'gpu_hist'
        if self.multi == 1:                                                     # 根据分类任务，设置目标函数及评价指标
            self.params['objective'] = 'multi:softmax'
            self.params['eval_metric'] = 'mlogloss'

        self.cvr = xgb.cv(params=self.params,                                   
                          dtrain=self.dtrain,
                          num_boost_round=self.n_rounds,
                          nfold=10,
                          stratified=True,
                          metrics='aucpr' if self.balanced==0 else 'auc',
                          maximize=True,
                          early_stopping_rounds=self.early_stopping,
                          verbose_eval=self.verbose,
                          seed=self.seed)                                       # cross-validation
        self.n_rounds = self.cvr.shape[0]                                       # 记录最佳训练回合数 

        duration = time.time() - start_time
        message = 'cross validation done with number of rounds: %d \tduration: %.3f s.' % (self.n_rounds, duration)
        print(message)
        
        return None

    def train(self, path_model=None):
        """ 模型训练器.

        输入:
            path_model: 模型保存地址, str.              
        """
        try:                                                                    # 查看是否进行超参设定，如没有，使用默认参数
            print(json.dumps(self.params, indent=4))
            message = 'number of training rounds: %d.' % self.n_rounds
            print(message)
        except Exception as e:
            message = 'no hpyter parameters assigned and default assigned.'
            print(message)
            self.algorithm()
            print(json.dumps(self.params, indent=4))

        self.bst = xgb.train(params=self.params,
                             dtrain=self.dtrain,
                             evals=[(self.dtrain, 'train')],
                             num_boost_round=self.n_rounds,
                             verbose_eval=self.verbose)                         # 训练模型

        if path_model == None:                                                  # 保存模型
            pass
        else:
            pickle.dump(self.bst, open(path_model, 'wb'))
            print('model saved in path: %s' % path_model)

        self.prediction[self.indcol] = self.data[self.indcol]                   # 预测训练集数据 
        self.prediction['prob'] = self.bst.predict(self.dtrain)
        message = 'prediction done.'
        print(message)
        return None 

    def evaluate(self, path_model):
        """模型评价器.

        输入:
            path_model: 待评价模型保存地址, str.

        输出:
            模型评价值
        """
        self.bst = pickle.load(open(path_model, 'rb'))                          # 加载模型
        message = 'model loaded from path: %s' % path_model
        print(message)
        return self.bst.eval(self.dtrain)                                       # 输出评价

    def predict(self, path_model, path_result=None):
        """模型预测器.

        输入:
            path_model: 模型保存地址, str.
            path_result: 预测结果保存地址, str.

        输出:
            prediction: 预测结果, pandas.DataFrame.
        
        """
        self.bst = pickle.load(open(path_model, 'rb'))                          # 加载模型
        message = 'model loaded from path: %s' % path_model
        print(message)

        self.prediction[self.indcol] = self.data[self.indcol]                   # 进行预测
        self.prediction['prob'] = self.bst.predict(self.dtest)
        message = 'prediction done.'
        print(message)

        if path_result == None:                                                 # 保存预测结果
            pass
        else:
            self.prediction.to_csv(path_result, index=False)
            message = 'results saved in path: %s' % path_result
            print(message)
        return None

    def retrain(self, path_model, path_model_update=None):
        """模型持续训练器.

        输入:
            path_model: 初始模型保存地址, str.
            path_model_update: 更新模型保存地址, str.
        """
        try:                                                                    # 查看是否进行超参设定，如没有，使用默认参数
            message = 'number of training rounds: %d' % self.n_rounds
            print(message)
        except Exception as e:
            message = 'no hpyter parameters assigned and default assigned.'
            print(message)
            self.algorithm()
            print(json.dumps(self.params, indent=4))

        self.bst = pickle.load(open(path_model, 'rb'))                          # 加载已有模型
        message = 'model loaded from path: %s' % path_model
        print(message)

        self.bst.update(dtrain=self.dtrain, iteration=self.n_rounds)            # 继续训练
        message = 'model updated.'
        print(message)

        if path_model_update == None:
            pass
        else:
            pickle.dump(self.bst, open(path_model_update, 'wb'))
            print('model saved in path: %s' % path_model_update)

        self.prediction[self.indcol] = self.data[self.indcol]
        self.prediction['prob'] = self.bst.predict(self.dtrain)
        message = 'prediction done.'
        print(message)
        return None

    def learning_curve(self):
        """学习曲线, 模型训练后提供学习曲线.
        """
        if len(self.cvr) == 0:                                                  # 查看是否已有训练结果
            return 'no models trained, no learning curves.'

        plt.figure(figsize=(10, 4))
        plt.plot(self.cvr[self.cvr.columns[0]])                                 # 测试曲线
        plt.plot(self.cvr[self.cvr.columns[2]])                                 # 训练曲线
        plt.title('learning curve')
        plt.xlabel('number of rounds')
        plt.ylabel('auc')
        plt.legend([self.cvr.columns[0], self.cvr.columns[2]])
        plt.grid() 
        plt.show()

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

        test_target = self.data[self.target]

        prob = self.prediction['prob']

        plt.figure(figsize=(6, 5.5))                                    
        self.prediction['prob'].hist(bins=100)                                  # 预测分布直方图
        plt.title('distribution of predictions')

        vis = Visual(test_target=test_target, test_predprob=prob)
        vis.CM()                                                                # 混淆矩阵
        vis.ROC()                                                               # ROC 曲线
        vis.PR()                                                                # PR 曲线
        return None 
