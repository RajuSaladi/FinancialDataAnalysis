import pandas as pd
from pandas import Series, DataFrame, Panel
import seaborn as sns

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


#from matplotlib.mpl_finance import candlestick_ohlc
from mpl_finance.mpl_finance import candlestick_ohlc
#from mpl_finance.mpl_finance import candlestick2_ohlc
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import datetime as dt

import matplotlib.ticker as mticker

from CommonTensorflowFunctions import inputDataProcessing

import os
import time
import pdb


class FinanceDataFunctions:

	def plotCandleStickGraph(self,df_ohlc,outputPlotFolder,movingAverageWindowSize = None,SHOWPLOT=0,plotTitle = None):

		#Making plot
		fig = plt.figure()
		ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)

		#Converts raw mdate numbers to dates
		ax1.xaxis_date()
		plt.xlabel("Date")
		#print(df_ohlc)
		#pdb.set_trace()
		#Making candlestick plot
		
		candlestick_ohlc(ax1,df_ohlc.values,width=1, colorup='g', colordown='k',alpha=0.75)
		fig.autofmt_xdate()
		# candlestick2_ohlc(ax1,df_ohlc.Open, df_ohlc.High, df_ohlc.Low, df_ohlc.Close,width=1, colorup='g', colordown='k',alpha=0.75)
		plt.ylabel("Price")

		plt.legend()


		if movingAverageWindowSize is not None:
			df_ohlc[str(movingAverageWindowSize)+"MovAvg"] = df_ohlc["Close"].rolling(movingAverageWindowSize).mean()
			ax1.plot(df_ohlc['Date'],df_ohlc[str(movingAverageWindowSize)+"MovAvg"])
	
		if(plotTitle is not None):
			plt.title(plotTitle)
		outputPlotFileName = os.path.join(outputPlotFolder,"CandlePlot_"+str(currentStockName)+".png")
		plt.savefig(outputPlotFileName)
		if SHOWPLOT is True:
			plt.show()

	def dataFrameWithMovingAverages(self,dF,movingAverageWindowSizeList = [10,30]):
		keyDataList = ["Open","High",'Low',"Close"]
		for currentWindowSize in movingAverageWindowSizeList:
			dF,keyDataList = self.addMovingAverageToDataFrame(dF,currentWindowSize,keyDataList)
		return dF,keyDataList
	
	def addMovingAverageToDataFrame(self,dF,movingAverageWindowSize,keyDataList):

		dF["Open_MA"+str(movingAverageWindowSize)] = dF["Open"].rolling(movingAverageWindowSize).mean()
		keyDataList.append("Open_MA"+str(movingAverageWindowSize))

		dF["Close_MA"+str(movingAverageWindowSize)] = dF["Close"].rolling(movingAverageWindowSize).mean()
		keyDataList.append("Close_MA"+str(movingAverageWindowSize))
		return dF,keyDataList

	def prepareDataForFinancePlots(self,currentCsvFilePath):
		df_ohlc = pd.read_csv(currentCsvFilePath,usecols = ["Date","Open","High",'Low',"Close"])
		df_ohlc = df_ohlc.dropna()
		df_ohlc["Date"] = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in df_ohlc["Date"]]
		df_ohlc["Date"] = [date2num(d) for d in df_ohlc["Date"]]
		
		df_ohlc["Open"] = df_ohlc["Open"].astype(int)
		df_ohlc["High"] = df_ohlc["High"].astype(int)
		df_ohlc["Low"] = df_ohlc["Low"].astype(int)
		df_ohlc["Close"] = df_ohlc["Close"].astype(int)
		return df_ohlc

	def dataStructuringForPredictionModel(self,dF,keyDataList,inputWindowSize):
		#xStructure = ["Open","High",'Low',"Close",MOVINGAVERAGELIST]
		dataX = []
		dataY = []
		for i in range(inputWindowSize,len(dF)):
			x = [[0]*(inputWindowSize-1)]*len(keyDataList)
			y = [0]*len(keyDataList)
			for z in range(0,len(keyDataList)):
				#x1 = [openValue for d in dF["Open"][(i-inputWindowSize):i]
				x[z] = self.getPreviousValueListOfDataFrame(dF,keyDataList[z],int(i-inputWindowSize),i-1)
				y[z] = self.getPreviousValueListOfDataFrame(dF,keyDataList[z],i,i+1)[0]
				#pdb.set_trace()
			dataX.append(x)
			dataY.append(y)
		return dataX,dataY

	def getPreviousValueListOfDataFrame(self,dF,category,lowerLimit,upperLimit):
		return [currentValue for currentValue in dF[category][lowerLimit:upperLimit]]
		

if __name__ == "__main__":


	finDataFunc = FinanceDataFunctions()
	dataProc = inputDataProcessing()

	INPUTDATAFOLDER = "D:\\StudyZone\\MachineLearning\\FinanceDeepLearning\\Data\\"
	OUTPUTFOLDER = "D:\\StudyZone\\MachineLearning\\FinanceDeepLearning\\OutputFolder\\"

	timeStr = time.strftime("%Y%m%d_%H%M%S")
	#OUTPUTFOLDER = os.path.join(OUTPUTFOLDER,timeStr)
	OUTPUTPLOTFOLDER = os.path.join(OUTPUTFOLDER,"Plots")
	DISPLAYCANDLEPLOT = 0
	MOVINGAVERAGE = 10
	MOVINGAVERAGELIST = [10,30]
	INPUTWINDOWSIZE = 10
	TESTDATARATIO = 0.1
	BATCHSIZE = 50

	if not os.path.exists(OUTPUTFOLDER):
		os.makedirs(OUTPUTFOLDER)

	if not os.path.exists(OUTPUTPLOTFOLDER):
		os.makedirs(OUTPUTPLOTFOLDER)

	csvFileList = os.listdir(INPUTDATAFOLDER)

	#for currentFile in csvFileList:
	if(1):
		currentFile = "EDELWEISS.NS.csv"
		# if not currentFile.endswith('.csv'):
			# continue
		currentStockName = currentFile.split(".NS.csv")[0]

		print("Currently processing Stock Data for "+str(currentStockName))

		currentCsvFilePath = os.path.join(INPUTDATAFOLDER,currentFile)
		if(DISPLAYCANDLEPLOT == 1):
			currentDF = finDataFunc.prepareDataForFinancePlots(currentCsvFilePath)
			outputPlotFileName = os.path.join(OUTPUTPLOTFOLDER,"CandlePlot_"+str(currentStockName)+".png")
			finDataFunc.plotCandleStickGraph(currentDF,OUTPUTPLOTFOLDER,MOVINGAVERAGE,SHOWPLOT=False,plotTitle = "CandleChart For "+str(currentStockName))

		dF = pd.read_csv(currentCsvFilePath,usecols = ["Date","Open","High","Low","Close"])
		dF = dF.dropna()
		dF,keyDataList = finDataFunc.dataFrameWithMovingAverages(dF,MOVINGAVERAGELIST)	
		dataX , dataY = finDataFunc.dataStructuringForPredictionModel(dF,keyDataList,INPUTWINDOWSIZE)

		trainInputDataQueue,testInputDataQueue,trainOutputQueue,testOutputQueue = dataProc.createPipelineForData(dataX,dataY,TESTDATARATIO,inputDataType = "float32",outputDataType = "float32")
		trainBatchX,trainBatchY = dataProc.makePipelineBatchWise(trainInputDataQueue,trainOutputQueue,BATCHSIZE)
		testBatchX,testBatchY = dataProc.makePipelineBatchWise(testInputDataQueue,testOutputQueue,BATCHSIZE)
		
		#pdb.set_trace()

		