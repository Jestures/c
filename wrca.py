import streamlit as st
import pandas as pd
from datetime import date
from yahoo_finance import Share as sh
from yahoo_fin import stock_info as si
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


st.set_page_config(page_title='Stock Prediction using ML', page_icon=' :smiley: ')

def main():

	st.title("Welcome to Predict Future of Finance.")

	menu = ["Recommendations","Currencies","Crypto Currencies","Analization","Stock Prediction using ML","Crypto Prediction using ML"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Recommendations":
		st.header("Recommendations ")
		
		si.get_day_most_active()
		st.subheader("Today's Most Active Users")
		active = si.get_day_most_active()
		st.write(active)
		

		def plot_raw_data():
			fig = go.Figure()
			fig.add_trace(go.Bar(x=active['Symbol'], y=active['Volume']))
			st.plotly_chart(fig)			
		plot_raw_data()	


		si.get_day_gainers()
		st.subheader("Today's Top Gainers")
		gainer = si.get_day_gainers()
		st.write (gainer)

		def plot_raw_data():
			fig = go.Figure()
			fig.add_trace(go.Bar(x=gainer['Symbol'],y=gainer['% Change']))
			st.plotly_chart(fig)			
		plot_raw_data()	

		si.get_day_losers()
		st.subheader("Today's Top Losers")
		loser = si.get_day_losers()
		st.write(loser)

		def plot_raw_data():
			fig = go.Figure()
			fig.add_trace(go.Bar(x=loser['Symbol'],y=loser['% Change']))
			st.plotly_chart(fig)			
		plot_raw_data()

		si.get_futures()
		st.subheader("Today's Future Stocks")
		future = si.get_futures()
		st.write(future)


		def plot_raw_data():
			fig = go.Figure()
			fig.add_trace(go.Bar(x=future['Symbol'],y=future['% Change']))
			st.plotly_chart(fig)			
		plot_raw_data()



	elif choice == "Currencies":
    		
			si.get_currencies()
			st.subheader("Today's Top Currencies ")
			currency = si.get_currencies()
			st.write(currency)

			def plot_raw_data():
				fig = go.Figure()
				fig.add_trace(go.Bar( x=currency['Symbol'],y=currency['% Change']))
				st.plotly_chart(fig)			
			plot_raw_data()
			

	elif choice == "Crypto Currencies":
    		
			si.get_top_crypto()
			st.subheader("Today's Top Crypto: ")
			crypto = si.get_top_crypto()
			st.write(crypto)

			st.subheader("Top Crypto's Price: ")

			def plot_raw_data():
				fig = go.Figure()
				fig.add_trace(go.Bar(x=crypto['Symbol'],y=crypto['Price (Intraday)']))
				st.plotly_chart(fig)			
			plot_raw_data()

			st.subheader("Top Crypto's Change (%): ")

			def plot_raw_data():
				fig = go.Figure()
				fig.add_trace(go.Bar(x=crypto['Symbol'],y=crypto["% Change"]))
				st.plotly_chart(fig)			
			plot_raw_data()

	elif choice == "Analization":
    		
	    st.header("Stock Analization using ML")

	    START = "2015-01-01"
	    TODAY = date.today().strftime("%Y-%m-%d")

	    selected_stock1 = st.text_input("Type 1st Stocks's name...")
	    selected_stock2 = st.text_input("Type 2nd Stocks's name...")

	    submit = st.button('Search')
	    if submit:

		    msft = yf.Ticker(selected_stock1) 
		    name1 = msft.info['longName']

		    msft = yf.Ticker(selected_stock2) 
		    name2 = msft.info['longName']

		    si.get_live_price(selected_stock1)
		    st.write("Live Price of " + name1 + " : $" , si.get_live_price(selected_stock1))
            

		    si.get_live_price(selected_stock2)
		    st.write("Live Price of " + name2 + " : $" , si.get_live_price(selected_stock2))

            
		    def load_data(ticker):
			    data = yf.download(ticker, START, TODAY)
			    data.reset_index(inplace=True)
			    return data

                
		    data = load_data(selected_stock1)
		    data1 = load_data(selected_stock2)


		    st.subheader('Raw data of '+ name1)
		    st.write(data.tail())
		    st.subheader('Raw data of '+ name2)
		    st.write(data1.tail())


			# Plot Volume of the companies

		    def plot_raw_data():
		        fig = go.Figure()
		        fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name="Volume of "+name1))				
		        fig.add_trace(go.Bar(x=data1['Date'], y=data1['Volume'],name="Volume of "+name2))
		        fig.layout.update(title_text='Analization of Volumes : ', xaxis_rangeslider_visible=True)
		        st.plotly_chart(fig)
                
		    plot_raw_data()


            # Plot Open & Closed Data
            
		    def plot_raw_data():
		        fig = go.Figure()
		        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open Price"))
		        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closed Price"))
		        fig.add_trace(go.Scatter(x=data1['Date'], y=data1['Open'], name="Open Price"))
		        fig.add_trace(go.Scatter(x=data1['Date'], y=data1['Close'], name="Closed Price"))
		        fig.layout.update(title_text='Analization of Open & Closed Data : ', xaxis_rangeslider_visible=True)
		        st.plotly_chart(fig)
                
		    plot_raw_data()

			# Plot High & low of the companies

		    def plot_raw_data():
		        fig = go.Figure()
		        fig.add_trace(go.Line(x=data['Date'], y=data['High'], name="High of "+name1))	
		        fig.add_trace(go.Line(x=data['Date'], y=data['Low'], name="Low of "+name1))				
		        fig.add_trace(go.Line(x=data1['Date'], y=data1['High'],name="High of "+name2))			
		        fig.add_trace(go.Line(x=data1['Date'], y=data1['Low'],name="Low of "+name2))
		        fig.layout.update(title_text='Analization of High & Low : ', xaxis_rangeslider_visible=True)
		        st.plotly_chart(fig)      

		    plot_raw_data()


	elif choice == "Stock Prediction using ML":
		st.header("Stock Prediction using ML")

		START = "2010-01-01"
		TODAY = date.today().strftime("%Y-%m-%d")

		selected_stock = st.text_input("Type Stocks's name...")

		submit = st.button('Search')
		if submit:
    			
			
			def load_data(ticker):
				data = yf.download(ticker, START, TODAY)
				data.reset_index(inplace=True)
				return data

			data_load_state = st.text('Loading data...')
			data = load_data(selected_stock)
			data_load_state.text('Loading data... done!')

			
			si.get_live_price(selected_stock)
			st.write("Live Price : ", si.get_live_price(selected_stock))
			
			si.get_market_status()
			st.write("Market state : ", si.get_market_status())

			n_years = st.slider("Years of prediction:", 1, 10)
			period = n_years * 365


			st.subheader('Raw data')
			st.write(data.tail())

			# Plot raw data
			
			def plot_raw_data():
				fig = go.Figure()
				fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open Price"))
				fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closed Price"))
				fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
				st.plotly_chart(fig)
				
			plot_raw_data()

			# Predict forecast with Prophet.
			df_train = data[['Date','Close']]
			df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

			m = Prophet()
			m.fit(df_train)
			future = m.make_future_dataframe(periods=period)
			forecast = m.predict(future)

			# Show and plot forecast
			st.subheader('Forecast data')
			st.write(forecast.tail())
				
			st.write(f'Forecast plot for {n_years} years')
			fig1 = plot_plotly(m, forecast)
			st.plotly_chart(fig1)

			st.write("Forecast components")
			fig2 = m.plot_components(forecast)
			st.write(fig2)

	elif choice == "Crypto Prediction using ML":
			st.header("Crypto Prediction using ML")

			START = "2010-01-01"
			TODAY = date.today().strftime("%Y-%m-%d")

			selected_crypto = st.text_input("Type Crypto Currency's name...")

			submit = st.button('Search')
			if submit:
					
				
				def load_data(ticker):
					data = yf.download(ticker, START, TODAY)
					data.reset_index(inplace=True)
					return data

				data_load_state = st.text('Loading data...')
				data = load_data(selected_crypto)
				data_load_state.text('Loading data... done!')
							
				si.get_live_price(selected_crypto)
				st.write("Live Price : ", si.get_live_price(selected_crypto))
				
				si.get_market_status()
				st.write("Market state : ", si.get_market_status())

				n_years = st.slider("Years of prediction:", 1, 10)
				period = n_years * 365


				st.subheader('Raw data')
				st.write(data.tail())

				# Plot raw data
				
				def plot_raw_data():
					fig = go.Figure()
					fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name="Highest"))
					fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name="Lowest"))
					fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
					st.plotly_chart(fig)
					
				plot_raw_data()

				# Predict forecast with Prophet.
				df_train = data[['Date','Close']]
				df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

				m = Prophet()
				m.fit(df_train)
				future = m.make_future_dataframe(periods=period)
				forecast = m.predict(future)

				# Show and plot forecast
				st.subheader('Forecast data')
				st.write(forecast.tail())
					
				st.write(f'Forecast plot for {n_years} years')
				fig3 = plot_plotly(m, forecast)
				st.plotly_chart(fig3)

				st.write("Forecast components")
				fig4 = m.plot_components(forecast)
				st.write(fig4)


if __name__ == '__main__':
	main()
