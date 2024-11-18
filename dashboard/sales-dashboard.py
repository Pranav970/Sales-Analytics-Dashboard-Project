import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

class SalesDashboard:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        
    def render_dashboard(self):
        st.title('Sales Analytics Dashboard')
        
        # Sidebar for filters
        st.sidebar.header('Filters')
        date_range = st.sidebar.date_input('Select Date Range', 
                                           [self.df['order_date'].min(), 
                                            self.df['order_date'].max()])
        category_filter = st.sidebar.multiselect(
            'Select Product Categories', 
            self.df['product_category'].unique()
        )
        
        # Filter data
        filtered_df = self.filter_data(date_range, category_filter)
        
        # Dashboard Sections
        self.sales_trend_section(filtered_df)
        self.product_performance_section(filtered_df)
        self.geographic_analysis_section(filtered_df)
    
    def filter_data(self, date_range, category_filter):
        df_filtered = self.df[
            (self.df['order_date'].dt.date >= date_range[0]) & 
            (self.df['order_date'].dt.date <= date_range[1])
        ]
        
        if category_filter:
            df_filtered = df_filtered[df_filtered['product_category'].isin(category_filter)]
        
        return df_filtered
    
    def sales_trend_section(self, df):
        st.header('Sales Trends')
        monthly_sales = df.groupby(df['order_date'].dt.to_period('M'))['revenue'].sum().reset_index()
        monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)
        
        fig = px.line(monthly_sales, x='order_date', y='revenue', 
                      title='Monthly Revenue Trend')
        st.plotly_chart(fig)
    
    def product_performance_section(self, df):
        st.header('Product Performance')
        product_performance = df.groupby('product_category').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        
        fig = px.bar(product_performance, x='product_category', y='revenue',
                     hover_data=['quantity', 'profit_margin'],
                     title='Revenue by Product Category')
        st.plotly_chart(fig)
    
    def geographic_analysis_section(self, df):
        st.header('Geographic Sales Analysis')
        geo_sales = df.groupby('customer_country')['revenue'].sum().reset_index()
        
        fig = px.choropleth(geo_sales, 
                             locations='customer_country', 
                             locationmode='country names',
                             color='revenue',
                             title='Sales Distribution by Country')
        st.plotly_chart(fig)

def main():
    dashboard = SalesDashboard('../data/cleaned_sales_data.csv')
    dashboard.render_dashboard()

if __name__ == '__main__':
    main()
