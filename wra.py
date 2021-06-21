import streamlit as st
from datetime import date
from yahoo_fin import stock_info as si
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


st.set_page_config(page_title='Stock Prediction using ML', page_icon=":smily:")

def main():

	st.title("Welcome to Predict Future of Finance.")

	#----------Menu----------#

	menu = ["Recommendations","Analization","Stock Prediction using ML"]
	choice = st.sidebar.selectbox("Menu",menu)

#----------------------Recommendation----------------------#

	if choice == "Recommendations":
		st.header("Recommendations ")
		
	#----------Fetching Data of Most Active Users----------#

		si.get_day_most_active()
		st.subheader("Today's Most Active Users")
		active = si.get_day_most_active()
		st.write(active)
		
	#----------Plotting Data of Most Active Users----------#

		def plot_raw_data():
    			
			fig = go.Figure()
			fig.add_trace(go.Bar(x=active['Symbol'], y=active['Volume']))
			fig.layout.update(width=900, height=550, hovermode='x')
			st.plotly_chart(fig)	

		plot_raw_data()	

	#----------Fetching Data of Top Gainers----------#

		si.get_day_gainers()
		st.subheader("Today's Top Gainers")
		gainer = si.get_day_gainers()
		st.write (gainer)

	#----------Plotting Data of Top Gainers----------#

		def plot_raw_data():
    			
			fig = go.Figure()
			fig.add_trace(go.Bar(x=gainer['Symbol'],y=gainer['% Change']))
			fig.layout.update( width=900, height=550, hovermode='x')
			st.plotly_chart(fig)	

		plot_raw_data()	

	#----------Fetching Data of Top Losers----------#

		si.get_day_losers()
		st.subheader("Today's Top Losers")
		loser = si.get_day_losers()
		st.write(loser)

	#----------Plotting Data of Top Losers----------#

		def plot_raw_data():
    			
			fig = go.Figure()
			fig.add_trace(go.Bar(x=loser['Symbol'],y=loser['% Change']))
			fig.layout.update(width=900, height=550, hovermode='x')
			st.plotly_chart(fig)

		plot_raw_data()

	#----------Fetching Data of Futures Stocks----------#

		si.get_futures()
		st.subheader("Today's Stocks for Future")
		future = si.get_futures()
		st.write(future)

	#----------Plotting Data of Futures Stocks----------#

		def plot_raw_data():
    			
			fig = go.Figure()
			fig.add_trace(go.Bar(x=future['Symbol'],y=future['% Change']))
			fig.layout.update(width=900, height=550, hovermode='x')
			st.plotly_chart(fig)

		plot_raw_data()

#------------------------Analization------------------------#

	elif choice == "Analization":
    		
	    st.header("Stock Analization using ML")

		#-------------Starting Date and Ending Date------------#
	    START = "2015-01-01"
	    TODAY = date.today().strftime("%Y-%m-%d")


		#---Input for First Stock---#

	    selected_stock1 = st.text_input("Type 1st Stocks's name...")

		#---Input for Second Stock---#

	    selected_stock2 = st.text_input("Type 2nd Stocks's name...")


		#---Submit Button---#

	    submit = st.button('Search')			
	    if submit:


			#---Fetching name of First Stock---#

		    msft = yf.Ticker(selected_stock1) 
		    name1 = msft.info['longName']

			#---Fetching name of Second Stock---#

		    msft = yf.Ticker(selected_stock2) 
		    name2 = msft.info['longName']


			#---Fetching Live Price of First Stock---#

		    si.get_live_price(selected_stock1)
		    st.write("Live Price of " + name1 + " : $" , si.get_live_price(selected_stock1))
            
			#---Fetching Live Price of Second Stock---#

		    si.get_live_price(selected_stock2)
		    st.write("Live Price of " + name2 + " : $" , si.get_live_price(selected_stock2))


			#-----Fetching Raw data-----#
            
		    def load_data(ticker):
			    data = yf.download(ticker, START, TODAY)
			    data.reset_index(inplace=True)
			    return data

                
		    data = load_data(selected_stock1)
		    data1 = load_data(selected_stock2)


			#-----Printing of Raw Data of First Stock-----#

		    st.subheader('Raw data of '+ name1)
		    st.write(data.tail())

			#-----Printing of Raw Data of Second Stock-----#

		    st.subheader('Raw data of '+ name2)
		    st.write(data1.tail())



		#----------Plot Volume of the companies----------#

		    def plot_raw_data():
    				
		        fig = go.Figure()
		        fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name="Volume of "+name1))				
		        fig.add_trace(go.Bar(x=data1['Date'], y=data1['Volume'],name="Volume of "+name2))
		        fig.layout.update(title_text='Analization of Volume Data : ', xaxis_rangeslider_visible=True, width=1000, height=600, hovermode='x')
		        st.plotly_chart(fig)
                
		    plot_raw_data()


        #----------Plot Open & Closed Data----------#
            
		    def plot_raw_data():
    				
		        fig = go.Figure()
		        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open Price of "+name1))
		        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closed Price of "+name1))
		        fig.add_trace(go.Scatter(x=data1['Date'], y=data1['Open'], name="Open Price of "+name2))
		        fig.add_trace(go.Scatter(x=data1['Date'], y=data1['Close'], name="Closed Price of "+name2))
		        fig.layout.update(title_text='Analization of Open & Close Data : ', xaxis_rangeslider_visible=True, width=1000, height=600, hovermode='x')
		        st.plotly_chart(fig)
                
		    plot_raw_data()

		#----------Plot High & low of the companies----------#

		    def plot_raw_data():
    				
		        fig = go.Figure()
		        fig.add_trace(go.Line(x=data['Date'], y=data['High'], name="High of "+name1))	
		        fig.add_trace(go.Line(x=data['Date'], y=data['Low'], name="Low of "+name1))				
		        fig.add_trace(go.Line(x=data1['Date'], y=data1['High'],name="High of "+name2))			
		        fig.add_trace(go.Line(x=data1['Date'], y=data1['Low'],name="Low of "+name2))
		        fig.layout.update(title_text='Analization of High & Low Data : ', xaxis_rangeslider_visible=True, width=1000, height=600, hovermode='x')
		        st.plotly_chart(fig)      

		    plot_raw_data()

#-----------------Stock Prediction using ML-----------------#

	elif choice == "Stock Prediction using ML":
		st.header("Stock Prediction using ML")


		#-------------Starting Date and Ending Date------------#

		START = "2010-01-01"
		TODAY = date.today().strftime("%Y-%m-%d")


		#---Input for Stock's name---#

		selected_stock = st.text_input("Type Stocks's name...")
	

		#---Slider of Year of prediction---#

		n_years = st.slider("Years of prediction:", 1, 10)
		period = n_years * 365	


		#---Submit Button---#

		submit = st.button('Search')


		if submit:

			@st.cache
			def load_data(ticker):
    				
				data = yf.download(ticker, START, TODAY)
				data.reset_index(inplace=True)
				return data

			data_load_state = st.text('Loading data...')
			data = load_data(selected_stock)
			data_load_state.text('Loading data... done!')


			#---Fetching name of Company---#

			msft = yf.Ticker(selected_stock) 
			name1 = msft.info['longName']


			#---Fetching Live Price of First Stock---#

			si.get_live_price(selected_stock)
			st.write("Live Price of "+ name1+" : $", si.get_live_price(selected_stock))
			

			#---Fetching Market Status of First Stock---#

			si.get_market_status()
			st.write("Market state : ", si.get_market_status())


			#-----Printing Raw Data-----#

			st.subheader('Raw data')
			st.write(data.tail())

			
			#----------Plot Open & Closed Data----------#

			def plot_raw_data():
    				
				fig = go.Figure()
				fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open Price"))
				fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closed Price"))
				fig.layout.update(title_text='Graphical representation of Open & Closed Data : ', xaxis_rangeslider_visible=True, width=1000, height=600, hovermode='x')
				st.plotly_chart(fig)
				
			plot_raw_data()


			#------Training of Data  Prophet------#

			df_train = data[['Date','Close']]
			df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

			m = Prophet()
			m.fit(df_train)
			future = m.make_future_dataframe(periods=period)
			forecast = m.predict(future)


			#------Show and plot forecasted data------
			
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
