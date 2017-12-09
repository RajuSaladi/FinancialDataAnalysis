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


import os
import time
import pdb


class FinanceDataFunctions:

	def plotCandleStickGraph(self,df_ohlc,outputPlotFileName,movingAverage = None,SHOWPLOT=0,plotTitle = None):

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


		if movingAverage is not None:
			df_ohlc[str(movingAverage)+"MovAvg"] = df_ohlc["Close"].rolling(movingAverage).mean()
			ax1.plot(df_ohlc['Date'],df_ohlc[str(movingAverage)+"MovAvg"])
	
		if(plotTitle is not None):
			plt.title(plotTitle)
		outputPlotFileName = os.path.join(outputPlotFolder,"CandlePlot_"+str(currentStockName)+".png")
		plt.savefig(outputPlotFileName)
		if SHOWPLOT is True:
			plt.show()


	def prepareDataForFinancePlots(self,currentCsvFilePath):
		df_ohlc = pd.read_csv(currentCsvFilePath,usecols = ["Date","Open","High",'Low',"Close"])
		df_ohlc = df_ohlc.dropna()
		df_ohlc['Date'] = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in df_ohlc['Date']]
		df_ohlc['Date'] = [date2num(d) for d in df_ohlc['Date']]
		
		df_ohlc["Open"] = df_ohlc["Open"].astype(int)
		df_ohlc["High"] = df_ohlc["High"].astype(int)
		df_ohlc["Low"] = df_ohlc["Low"].astype(int)
		df_ohlc["Close"] = df_ohlc["Close"].astype(int)
		return df_ohlc


if __name__ == "__main__":


	finDataFunc = FinanceDataFunctions()
	INPUTDATAFOLDER = "D:\\StudyZone\\MachineLearning\\FinanceDeepLearning\\Data\\"
	OUTPUTFOLDER = "D:\\StudyZone\\MachineLearning\\FinanceDeepLearning\\OutputFolder\\"

	timeStr = time.strftime("%Y%m%d_%H%M%S")
	OUTPUTFOLDER = os.path.join(OUTPUTFOLDER,timeStr)
	OUTPUTPLOTFOLDER = os.path.join(OUTPUTFOLDER,"Plots")
	MOVINGAVERAGE = 10

	if not os.path.exists(OUTPUTFOLDER):
		os.makedirs(OUTPUTFOLDER)

	if not os.path.exists(OUTPUTPLOTFOLDER):
		os.makedirs(OUTPUTPLOTFOLDER)

	csvFileList = os.listdir(INPUTDATAFOLDER)

	for currentFile in csvFileList:
		if not currentFile.endswith('.csv'):
			continue
		currentStockName = currentFile.split(".NS.csv")[0]
		print("Currently processing Stock Data for "+str(currentStockName))
		currentDF = finDataFunc.prepareDataForFinancePlots(os.path.join(INPUTDATAFOLDER,currentFile))

		outputPlotFileName = os.path.join(OUTPUTPLOTFOLDER,"CandlePlot_"+str(currentStockName)+".png")
		finDataFunc.plotCandleStickGraph(currentDF,OUTPUTPLOTFOLDER,MOVINGAVERAGE,SHOWPLOT=False,plotTitle = "CandleChart For "+str(currentStockName))


