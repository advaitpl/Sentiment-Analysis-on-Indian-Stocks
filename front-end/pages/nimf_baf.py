#Imports

from calendar import month
from email.utils import parsedate, parsedate_to_datetime
from unicodedata import name
import dateparser
import streamlit as st
import pandas as pd
#from dash import dcc 
#import oauth2client
import numpy as np
#from oauth2client.service_account import ServiceAccountCredentials
from gspread_pandas import Spread, Client
import gspread_pandas
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import tldextract
import dateutil.parser as parser
from torch import scatter

import dash

# # from googlesheetsdb import connect
# import googlesheetsdb
# from googlesheetsdb import connect



#GSpread

# scope = ['https://www.googleapis.com/auth/spreadsheets', 
# 'https://www.googleapis.com/auth/drive.file',
# 'https://www.googleapis.com/auth/drive']

# config_dir = 'D:\\Downloads\\Sentiment analysis\\backend\\Sentiment analysis\\Output CSVs\\Google Sheet-GSpread API stuff'

# config = gspread_pandas.conf.get_config(conf_dir=config_dir,
# file_name='credentials.json.json')

# s = gspread_pandas.spread.Spread("url here", config = config)

import gspread

import dash

from oauth2client.service_account import ServiceAccountCredentials
# # from googlesheetsdb import connect
# import googlesheetsdb
# from googlesheetsdb import connect
# from google.colab import drive
# drive.mount('/content/drive',force_remount=True)
# from google.colab import data_table
# data_table.enable_dataframe_formatter()


#GSpread

# scope = ['https://www.googleapis.com/auth/spreadsheets', 
# 'https://www.googleapis.com/auth/drive.file',
# 'https://www.googleapis.com/auth/drive']

# config_dir = 'D:\\Downloads\\Sentiment analysis\\backend\\Sentiment analysis\\Output CSVs\\Google Sheet-GSpread API stuff'

# config = gspread_pandas.conf.get_config(conf_dir=config_dir,
# file_name='credentials.json.json')

# s = gspread_pandas.spread.Spread("1wYA3OyT0biSr6_eqWShtHuLS9CvfHRzhZ_xPEIVQzPI", config = config)

scope = ['https://www.googleapis.com/auth/spreadsheets', 
'https://www.googleapis.com/auth/drive.file',
'https://www.googleapis.com/auth/drive']

#master_path = "/content/drive/MyDrive/Nippon Sentiment Analyzer/"
config_dir = 'D:\\Downloads\\Sentiment analysis\\backend\\Sentiment analysis\\Output CSVs\\Google Sheet-GSpread API stuff'

config = gspread_pandas.conf.get_config(conf_dir=config_dir,
   file_name='credentials.json.json')

creds = ServiceAccountCredentials.from_json_keyfile_name(f'{config_dir}\\credentials.json.json',
                                             scope)
client = gspread.authorize(creds)
# config = gspread_pandas.conf.get_config(conf_dir=f'{master_path}Output CSVs/Google Sheet-GSpread API stuff/',
#                                file_name='credentials.json.json')
s = gspread_pandas.spread.Spread("11z53lQklRn_3yl55XrJbXVLUjiqdZHQhK9qf-PBkXvE", config = config, sheet="nimf-baf")



#Streamlit


def main():

    ### STREAMLIT CONTENT STARTS FROM HERE ###

    hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.title('Polarity Analysis')
    st.subheader("News articles' sentiment polarity labelled between -100 (most negative) to 100 (most positive)")

    # Reading in the data
    raw = s.sheet_to_df(sheet="nimf-baf")

    df = raw.copy(deep=True)
    st.dataframe(df)
 

    # Cleaning data

    #df['Date'] = pd.to_datetime(df['Date'],format="%d/%m/%Y", errors='coerce')
    
    df['Date'] = pd.to_datetime(df['Date'],infer_datetime_format=True, dayfirst=True, errors='coerce')
    # # # Initializing an unknown format date string
    # date_string = "###########"
    
    # # # Calling the parser to parse the above
    # # # specified unformatted date string
    # # # into a datetime objects
    # date_times = parser.parse(date_string)


    df = df.astype({"Name": str, "GNews": str,"URL": str,
    "Title": str, "Description": str, "Text": str, 
    "TextPolarity": int, "TextSentiment": str,
    "DescriptionPolarity": int, "DescriptionSentiment": str})

    df.sort_values(by=['Name', 'Date'], inplace=True)
    df['TextPolarity'].where(df['Text']!="none", df['DescriptionPolarity'], inplace=True)
    df['House'] = df['URL'].apply(lambda x: tldextract.extract(x)[1])

    ##### FEW COMPANY #####

    ### iNPUTS ###

    st.header("Stock view")
    st.caption("Suitable for understanding the sentiment for few companies")

    with st.form(key='few-companies'):
        st.write("Inputs")

        ##### Date is COMMENTED OUT AS IS NOT NEEDED SLIDER ADDED
        # start_date_few = st.date_input('Start date', value=datetime.today() - timedelta(7))
        # end_date_few = st.date_input('End date')

        # if start_date_few < end_date_few:
        #     st.success('Start date: `%s`\n\nEnd date:`%s`' %
        #             (start_date_few, end_date_few))
        # else:
        #     st.error('Error: End date must fall after start date.')

        # start_date_few = start_date_few.strftime("%Y-%m-%d")
        # end_date_few = end_date_few.strftime("%Y-%m-%d")

        # Company multi-select
        input_comps_few = st.multiselect(
        'Companies',
        df['Name'].unique().tolist(), df['Name'].unique().tolist()[1])

        # Media houses
        input_houses_few = st.multiselect(
        'Media Houses',
        df['House'].unique().tolist(), df['House'].unique().tolist())

        submitted = st.form_submit_button("Submit")

    ### OUTPUTS ###

    # Scatter dataframe

    scatterdf = df.copy(deep=True)
    scatterdf = scatterdf.astype({"Name": str, "GNews": str,"URL": str,
    "Title": str, "Description": str, "Text": str, 
    "TextPolarity": int, "TextSentiment": str,
    "DescriptionPolarity": int, "DescriptionSentiment": str, "House":str})
    scatterdf['Date'] = pd.to_datetime(scatterdf['Date'], infer_datetime_format=True, dayfirst=True, errors='coerce')
    #scatterdf['Date'] = pd.to_datetime(scatterdf['Date'], infer_datetime_format= True, errors='coerce')
    # scatterdf = scatterdf.query('Name in @input_comps_few')
    # scatterdf = scatterdf.query('House in @input_houses_few')
    #columns = scatterdf["Name", "TextPolarity", "House", "Date", "Title", "TextSentiment","House"]
    #date_mask_few = scatterdf['Date'].apply(lambda x : if x > start_date_few and x< end_date_few)
    #(scatterdf['Date']>start_date_few)&(scatterdf['Date']<end_date_few)
    #date_mask_few = scatterdf.loc[(scatterdf['Date']>start_date_few) &(scatterdf['Date']<end_date_few),['Name','TextPolarity','Title','Date','DescriptionSentiment','DescriptionPolarity','TextSentiment','House']]
    #mask_dates_few = (scatterdf['Date']>start_date_few) &(scatterdf['Date']<end_date_few)
    #scatterdf.loc[(scatterdf['Date']>start_date_few) &(scatterdf['Date']<end_date_few)]
    #rslt_df = scatterdf[scatterdf['Date'].isin(mask_dates_few)] 
    #scatterdf['Date'] = pd.to_datetime(date_mask_few,format="%d/%m/%Y", errors='coerce')
    #dates_input = rslt_df["Date"].values.astype('datetime64[ns]')
    #scatter_query= scatterdf[['Date']][(scatterdf['Date']>start_date_few) &(scatterdf['Date']<end_date_few)]
    #mask_dates_few= scatterdf[(scatterdf.Date >= start_date_few) & (scatterdf.Date < end_date_few)]
    #scatterdf= scatterdf.loc[mask_dates_few,['Name','TextPolarity','Title','DescriptionSentiment','Date','DescriptionPolarity','TextSentiment','House']]
    #scatterdf =scatterdf.query[scatterdf['Date']>start_date_few,'Date']=Date
    #scatterdf = date_mask_few
    #scatter_array = scatterdf.loc[scatterdf["Date"] > start_date_few, "Name"]
    scatterdf['Dates']=scatterdf['Date']
    scatterdf['Dates'] = pd.to_datetime(scatterdf['Date'], infer_datetime_format=True, errors='coerce')
    #scatter_array= (scatterdf['Date']>start_date_few)&(scatterdf['Date']<end_date_few)
    #scatterdf = scatterdf.loc[scatter_array,['Name','TextPolarity','Title','DescriptionSentiment','Dates','DescriptionPolarity','TextSentiment','House']]
    #scatterdf = scatterdf.loc[(scatterdf['Dates']>start_date_few)&(scatterdf['Dates']<end_date_few),['Name','TextPolarity','Title','DescriptionSentiment','Date','DescriptionPolarity','TextSentiment','House']]
    #scatterdf= scatterdf.query("Date  >= @start_date_few & Date < @end_date_few")
    #scatterdf=  scatterdf.query ('Date < @end_date_few')
    scatterdf = scatterdf.query('Name in @input_comps_few')
    scatterdf = scatterdf.query('House in @input_houses_few')
    scatterdf = scatterdf.fillna(method = 'backfill')
    
    #date_mask_few = date_mask_few['Date'].strftime("%Y-%m-%d")
    
    
    #scatterdf = scatterdf.loc[date_mask_few,['Name','TextPolarity','Title','TextSentiment','House']]
    
    #scatterdf = scatterdf.loc[date_mask_few,cols_scatterdf]
    #scatterdf = scatterdf.loc[date_mask_few][["Name", "TextPolarity", "House", "Date", "Title", "TextSentiment"]]
    # #scatterdf = scatterdf.query('Name' == input_comps_few and 'House'==input_houses_few, inplace=True)
   

    #scatterdf['Date'] = pd.to_datetime(scatterdf['Date'],format="%d/%m/%Y", errors='coerce')
    #date_mask_few["Date"] =  pd.to_datetime(date_mask_few["Date"], infer_datetime_format=True)
    #date_mask_few["Date"] = date_mask_few["Date"].apply(lambda x: dt.datetime.strptime(x,"%Y-%m-%d"))
    ## make Lineplot if compared against date
    st.dataframe(scatterdf)
    #scatterplot = go.Figure(go.scatter(x=scatterdf['Date'], y=scatterdf["Textpolarity"]))
    a=scatterdf['Date'].min()
    b=scatterdf['Date'].max()
    starting_day_of_current_year = datetime.now().date().replace(month=1, day=1)
    # Xaxis=scatterdf['Date']
    # Yaxis=scatterdf['TextPolarity']
    #scatterplot= go.Figure([go.scatter(x=scatterdf['Date'], y=scatterdf['TextPolarity'])])
    # scatterplot = px.scatter(scatterdf, x=Xaxis, y='TextPolarity', color='Name',
    #      hover_data=['Name', 'TextPolarity', 'Title', "House","Date"])
    # scatterplot = px.scatter(scatterdf, y='TextPolarity', color='Name',
    #        hover_data=['Name', 'TextPolarity', 'Title', "House","Date"])
        
    # scatterplot.update_layout(xaxis_title='Date', yaxis_title='Polarity')
    # #scatterplot.update_xaxes(type='date',range=[a,b])
    # scatterplot.update_yaxes(range=[-100, 100])
    # #scatterplot.update_traces(xbins_size="M1")
    # scatterplot.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y")
    # scatterplot.update_traces(marker_size=10)
    #fig = px.scatter(scatterdf,x=scatterdf["Date"],y=scatterdf["TextPolarity"],
    #        hover_data=['Name', 'TextPolarity', 'Title', 'House','Date'])
    # fig.update_layout(
    #     xaxis_title="Date",
    #     yaxis_title="TextPolarity",
    # )
    fig = px.scatter(scatterdf, x='Dates', y='TextPolarity', color='Name',
              hover_data ={'Name', 'TextPolarity', 'Title', 'House','Dates'},
              title='Text Polarity')

    fig.update_yaxes(range=[-100, 100])
    
    fig.update_layout(
    xaxis=dict(
        autorange=True,
        range=[a, b],
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count= 6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict( autorange= True,
            visible=True
        ),
        type="date"
    ))          
    #st.write(fig)
    #fig.update_yaxes(range[-100,100])
    #fig = go.Figure(go.Scatter(x=df['Date'], y=scatterdf['TextPolarity']))
    #animation_frame="Date", animation_group="TextPolarity",size="DescriptionSentiment", size_max=55,
    st.plotly_chart(fig, use_container_width=True,sharing="streamlit")


    # st.plotly_chart(fig, use_container_width=True,sharing="streamlit")

        #st.line_chart(scatterdf)
    # Scatterplot

    # scatterplot = px.scatter(scatterdf, x="Date", y="TextPolarity", color='Name',
    #     hover_data=['Name', 'TextPolarity', 'Title', "House"])
    # scatterplot.update_layout(xaxis_title='', yaxis_title='Polarity')
    # scatterplot.update_traces(marker_size=10)

    # st.plotly_chart(scatterplot, use_container_width=True,sharing="streamlit")


    ##### MANY COMPANIES #####
    
    ### INPUTS ###

    st.header("Portfolio View")
    st.caption("Suitable for understanding the sentiment of large number of companies")

    with st.form(key='many-companies'):
        st.write("Inputs")

        #Date
        start_date = st.date_input('Start date', value=datetime.today() - timedelta(7))
        end_date = st.date_input('End date')

        if start_date < end_date:
            st.success('Start date: `%s`\n\nEnd date:`%s`' %
                    (start_date, end_date))
        else:
            st.error('Error: End date must fall after start date.')

        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        
        # Company multi-select
        input_comps = st.multiselect(
         'Companies',
         df['Name'].unique().tolist(), df['Name'].unique().tolist()[:30])

        # Media houses
        input_houses = st.multiselect(
         'Media Houses',
         df['House'].unique().tolist(), df['House'].unique().tolist())

        submitted = st.form_submit_button("Submit")


    ### OUTPUT

    ## HISTOGRAM

    # Histogram datafrme
    histdf = df.copy()
    histdf = histdf.astype({"Name": str, "GNews": str,"URL": str,
    "Title": str, "Description": str, "Text": str, 
    "TextPolarity": int, "TextSentiment": str,
    "DescriptionPolarity": int, "DescriptionSentiment": str, "House":str})
    histdf['Date'] = pd.to_datetime(histdf['Date'], infer_datetime_format=True, dayfirst=True, errors='coerce')
    
    

    histdf['Dates']=histdf["Date"]
    histdf['Dates'] = pd.to_datetime(histdf['Date'], infer_datetime_format=True, dayfirst=True, errors='coerce')

    # histdf = df.loc[(histdf['Date'] >= start_date)
    #                  & (histdf['Date'] < end_date),["Name", "TextPolarity", "House", "Dates","DescriptionSentiment"]]
    # date_mask = (histdf['Date']>start_date)&(histdf['Date']<end_date)
    # histdf = histdf.loc[date_mask,["Name", "TextPolarity", "House", "Date"]]
    # c=histdf['Dates'].dropna().min()
    # d=histdf['Dates'].dropna().max()
    
    histdf = histdf.query('Name in @input_comps')
    histdf = histdf.query('House in @input_houses')
    #histdf =histdf.query ('Dates >= @start_date')
    #histdf =histdf.query ('Dates <= @end_date')
    

    #histdf['Dates'] = pd.to_datetime(histdf['Dates']).apply(lambda x: x.date())
    #histdf['time2'] = pd.to_datetime(histdf['Da']).apply(lambda x: x.time())
    c=histdf['Dates'].dropna().min()
    d=histdf['Dates'].dropna().max()

    #histdf = histdf.query('Date in @Date')
    st.dataframe(histdf)
    #Histogram plot
    hist_plot = px.histogram(histdf, x='TextPolarity', nbins=20,hover_data=histdf.columns, range_x=[-100,100],
        labels=dict(x="Sentiment interval", y="Count"))
    hist_plot.update_layout(xaxis_title='Polarity Intervals', yaxis_title='Count')
    hist_plot.update_layout(
                   xaxis=dict(color='gray',
                         linecolor='gray',
                         showgrid=False,
                         mirror=True,
                         rangeselector=dict(
                               buttons=list([
                                   dict(count=1,
                                        label='1d',
                                        step='day',
                                        stepmode='backward'),
                                   dict(count=7,
                                        label='1w',
                                        step='day',
                                        stepmode='backward'),
                                   dict(count=1,
                                        label='1m',
                                        step='month',
                                        stepmode='backward'),
                                    dict(count=1,
                                        label='1y',
                                        step='year',
                                        stepmode='backward'),
                                    dict(count=6,
                                        label='1y',
                                        step='month',
                                        stepmode='backward')])),
                         rangeslider=dict(visible=True, bordercolor='gray')))



#     hist_plot.update_layout(
#     xaxis=dict(
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1,
#                     step="day",
#                     stepmode="backward"),
#             ])
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#     )
#  )
    
    # hist_plot.update_layout(xaxis=dict(Date = st.slider("Date Range: ", min_value=c,   
    #                 max_value=d, value=[c,d], step=1,format="%d/%m/%Y")))
    #st.write("Start time:", Date)
    #         rangeselector=dict(
    #         buttons=list([
    #             dict(count=1,
    #                  label="1m",
    #                  step="month",
    #                  stepmode="backward"),
    #             dict(count= 6,
    #                  label="6m",
    #                  step="month",
    #                  stepmode="backward"),
    #             dict(count=1,
    #                  label="YTD",
    #                  step="year",
    #                  stepmode="todate"),
    #             dict(count=1,
    #                  label="1y",
    #                  step="year",
    #                  stepmode="backward"),
    #             dict(step="all")
    #         ])
    #     ),
    #     rangeslider=dict( autorange= True,
    #         visible=True
    #     ),
    #     type="date"
    # ))


    # Heatmap dataframe
    heatmapdf = histdf.copy()
    heatmapdf = heatmapdf.groupby(["Name", "Date"])["TextPolarity"].mean().unstack(level=1)

    #Heatmap plot
    heatmap_plot = px.imshow(heatmapdf,labels=dict(x="Date", y="Company", color="Polarity"))
    heatmap_plot.update_layout(yaxis=dict(tickmode='linear'),autosize=True)
    heatmap_plot.update_layout(xaxis_title='')
    heatmap_plot.update_layout(yaxis_title='Portfolio')
    heatmap_plot.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))

    # heatmap_plot.update_layout(
    #                      xaxis=dict(color='gray',
    #                      linecolor='gray',
    #                      showgrid=False,
    #                      mirror=True,
    #                      rangeselector=dict(
    #                            buttons=list([
    #                                dict(count=1,
    #                                     label='1d',
    #                                     step='day',
    #                                     stepmode='backward'),
    #                                dict(count=7,
    #                                     label='1w',
    #                                     step='day',
    #                                     stepmode='backward'),
    #                                dict(count=1,
    #                                     label='1m',
    #                                     step='month',
    #                                     stepmode='backward'),
    #                                 dict(count=1,
    #                                     label='1y',
    #                                     step='year',
    #                                     stepmode='backward'),
    #                                 dict(count=6,
    #                                     label='1y',
    #                                     step='month',
    #                                     stepmode='backward')])),
    #                                 type="date"
    #                     rangeslider=dict(visible=True, bordercolor='gray'))    

    ## COLUMN 1 PLOTS FOR AGGREGATE VIEW
    #col1, col2 = st.columns(2)

    #with col1:
    st.subheader("Aggregate Histogram")
    st.plotly_chart(hist_plot, use_container_width=True,sharing='streamlit')




        # hist_plot.update_layout(
        #     id='TimeFrame', # any name you'd like to give it
        #     step=1,                # number of steps between values
        #     min=2020,
        #     max=2022,
        #     value=[2020,2022],     # default value initially chosen
        #     dots=True,             # True, False - insert dots, only when step>1
        #     allowCross=False,      # True,False - Manage handle crossover
        #     disabled=False,        # True,False - disable handle
        #     pushable=2,            # any number, or True with multiple handles
        #     updatemode='mouseup',  # 'mouseup', 'drag' - update value method
        #     included=True,         # True, False - highlight handle
        #     vertical=False,        # True, False - vertical, horizontal slider
        #     verticalHeight=900,    # hight of slider (pixels) when vertical=True
        #     className='None',
        #     tooltip={'always visible':False,  # show current slider values
        #              'placement':'bottom'},
        #     ),
    








    #with col2:
    st.subheader("Aggregate Heatmap")
    st.plotly_chart(heatmap_plot, use_container_width=True,sharing="streamlit")






if __name__ == "__main__":
 main() 



    
