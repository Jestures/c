import streamlit as st
from datetime import date
from yahoo_fin import stock_info as si
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


def main():

	st.title("Welcome to Predict Future of Stocks.")

	menu = ["Home","Stock Prediction using ML"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Recommendations")
		
		si.get_day_most_active()
		st.subheader("Today's Most Active Users")
		st.write(si.get_day_most_active())

		si.get_day_gainers()
		st.subheader("Today's Top Gainers")
		st.write(si.get_day_gainers())

		si.get_day_losers()
		st.subheader("Today's Top Losers")
		st.write(si.get_day_losers())

	elif choice == "Stock Prediction using ML":
		st.subheader("Stock Prediction using ML")

		START = "2015-01-01"
		TODAY = date.today().strftime("%Y-%m-%d")

		selected_stock = st.text_input("Type Stocks's name...")

		submit = st.button('Search')
		if submit:
			
			si.get_live_price(selected_stock)
			st.write("Live Price : ", si.get_live_price(selected_stock))
			
			si.get_market_status()
			st.write("Market state : ", si.get_market_status())

			n_years = st.slider("Years of prediction:", 1, 10)
			period = n_years * 365


			
			def load_data(ticker):
				data = yf.download(ticker, START, TODAY)
				data.reset_index(inplace=True)
				return data

				
			data_load_state = st.text('Loading data...')
			data = load_data(selected_stock)
			data_load_state.text('Loading data... done!')

			st.subheader('Raw data')
			st.write(data.tail())

			# Plot raw data
			
			def plot_raw_data():
				fig = go.Figure()
				fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
				fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
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




if __name__ == '__main__':
	main()
