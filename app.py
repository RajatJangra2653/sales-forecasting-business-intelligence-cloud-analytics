import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from analytics.data import demo_data, validate_data, daily_series, load_gcs
from analytics.forecast import evaluate

st.set_page_config(page_title='SalesScope | Cloud Analytics', page_icon='📊', layout='wide')
st.markdown('''<style>.stApp {background:#f5f7fc;} h1,h2,h3 {color:#142445;}
[data-testid="stMetric"] {background:white;padding:18px;border:1px solid #e0e6f0;border-radius:12px;}
</style>''', unsafe_allow_html=True)
st.title('SalesScope')
st.caption('SALES FORECASTING & BUSINESS INTELLIGENCE · CLOUD ANALYTICS')

@st.cache_data
def sample():
    return demo_data()

@st.cache_data(show_spinner=False, max_entries=8)
def run_forecast(series, horizon):
    return evaluate(series, horizon)

with st.sidebar:
    st.header('Analytics workspace')
    source = st.radio('Data source', ['Synthetic demo', 'Upload CSV', 'Google Cloud Storage'])
    raw = None
    try:
        if source == 'Synthetic demo':
            raw = sample()
            st.info('Seeded synthetic data. Results do not demonstrate real business accuracy.')
        elif source == 'Upload CSV':
            upload = st.file_uploader('Sales CSV (up to 20 MB)', type='csv')
            if upload:
                if upload.size > 20*1024*1024:
                    raise ValueError('Upload exceeds 20 MB.')
                raw = pd.read_csv(upload)
        else:
            bucket = os.getenv('GCS_BUCKET', '')
            name = os.getenv('GCS_OBJECT', '')
            st.caption('Reads GCS_BUCKET and GCS_OBJECT using the server service account.')
            if st.button('Load configured cloud dataset'):
                st.session_state['cloud_data'] = load_gcs(bucket, name)
            raw = st.session_state.get('cloud_data')
        if raw is None:
            st.info('Choose a dataset to begin.')
            st.stop()
        data = validate_data(raw)
    except Exception as exc:
        st.error(f'Dataset could not be loaded: {exc}')
        st.stop()
    regions = st.multiselect('Regions', sorted(data.region.unique()), default=sorted(data.region.unique()))
    categories = st.multiselect('Categories', sorted(data.category.unique()), default=sorted(data.category.unique()))
    bounds = st.date_input('Analysis dates', (data.date.min().date(), data.date.max().date()),
                           min_value=data.date.min().date(), max_value=data.date.max().date())
    horizon = st.select_slider('Forecast horizon (days)', [7, 14, 28, 56], value=28)
    zero_fill = st.checkbox('Missing calendar days mean zero sales', value=False)
    st.download_button('Download sample CSV', sample().to_csv(index=False), 'sample_sales.csv', 'text/csv')

if len(bounds) != 2:
    st.info('Select both a start and end date.'); st.stop()
filtered = data[data.region.isin(regions) & data.category.isin(categories) &
                data.date.between(pd.Timestamp(bounds[0]), pd.Timestamp(bounds[1]))].copy()
if filtered.empty:
    st.warning('No sales match the selected filters.'); st.stop()
filtered['profit'] = filtered.revenue-filtered.cost
revenue = filtered.revenue.sum()
a,b,c,d = st.columns(4)
a.metric('Revenue', f'{revenue:,.0f}')
b.metric('Gross profit', f'{filtered.profit.sum():,.0f}')
c.metric('Gross margin', f'{100*filtered.profit.sum()/revenue:.1f}%' if revenue else 'N/A')
d.metric('Units sold', f'{filtered.units.sum():,.0f}')
st.caption('Amounts use the currency of the input dataset. Cost is assumed to be cost of goods sold.')
overview, forecasting, quality = st.tabs(['Business intelligence', 'Forecast laboratory', 'Data & methodology'])
with overview:
    trend = filtered.groupby('date', as_index=False)[['revenue','profit']].sum()
    st.plotly_chart(px.line(trend, x='date', y=['revenue','profit'], title='Revenue and gross profit over time'), use_container_width=True)
    left,right=st.columns(2)
    with left:
        st.plotly_chart(px.bar(filtered.groupby('region',as_index=False).revenue.sum(),x='region',y='revenue',color='region',title='Revenue by region'),use_container_width=True)
    with right:
        st.plotly_chart(px.bar(filtered.groupby('category',as_index=False)[['revenue','profit']].sum(),x='category',y=['revenue','profit'],barmode='group',title='Category performance'),use_container_width=True)
    heat=filtered.assign(weekday=filtered.date.dt.day_name(),month=filtered.date.dt.month).pivot_table(index='weekday',columns='month',values='revenue',aggfunc='mean')
    st.plotly_chart(px.imshow(heat, title='Average sales per input row · weekday × month',aspect='auto'),use_container_width=True)
    st.download_button('Export filtered sales',filtered.to_csv(index=False),'filtered_sales.csv','text/csv')
with forecasting:
    st.write('Models learn the selected segment and date range. Two expanding validation folds select the lowest-MAE model; the final holdout measures its performance.')
    if st.toggle('Train and evaluate models'):
        try:
            series=daily_series(filtered,zero_fill)
            with st.spinner('Evaluating chronological folds and fitting the selected model…'):
                winner,comparison,folds,test,scores,future=run_forecast(series,horizon)
            st.success(f'Selected model: {winner}')
            st.subheader('Validation comparison (mean across two folds)')
            st.dataframe(comparison,width='stretch')
            st.subheader('Untouched final holdout')
            st.json(scores)
            st.plotly_chart(px.line(test, title='Holdout: observed vs predicted'),use_container_width=True)
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=series.index[-180:],y=series.values[-180:],name='Observed',line_color='#52647f'))
            fig.add_trace(go.Scatter(x=future.index,y=future.upper,name='Upper band',line_width=0))
            fig.add_trace(go.Scatter(x=future.index,y=future.lower,fill='tonexty',fillcolor='rgba(52,105,240,.18)',name='Empirical error band',line_width=0))
            fig.add_trace(go.Scatter(x=future.index,y=future.forecast,name='Forecast',line_color='#3469f0'))
            fig.update_layout(title=f'Next {horizon} days · revenue forecast')
            st.plotly_chart(fig,use_container_width=True)
            st.caption('Band uses the 90th percentile of absolute validation errors pooled across horizons. It is exploratory, assumes stable errors, and has no guaranteed 90% future coverage.')
            uplift=st.slider('Planning scenario: revenue adjustment (%)',-30,30,0)
            scenario=future.copy()
            scenario['scenario']=scenario.forecast*(1+uplift/100)
            st.metric('Scenario total revenue',f'{scenario.scenario.sum():,.0f}')
            st.caption('Scenario adjustment is a planning assumption, not a causal estimate of pricing or marketing effects.')
            st.dataframe(scenario,width='stretch')
            st.download_button('Download forecast',scenario.to_csv(index_label='date'),'forecast.csv','text/csv')
            st.download_button('Download fold metrics',folds.to_csv(index=False),'validation_metrics.csv','text/csv')
        except ValueError as exc:
            st.warning(str(exc))
with quality:
    st.write(f'{len(filtered):,} input rows · {filtered.date.nunique():,} observed dates · {filtered.date.min().date()} to {filtered.date.max().date()}')
    st.dataframe(filtered.head(100),width='stretch')
    st.markdown('''**Input grain:** each row is a sales aggregate or transaction; repeated dates are summed. Repeated rows are retained because no transaction identifier is available.

**Models:** weekly seasonal naive baseline, regularized calendar-and-lag regression, and histogram gradient boosting with recursive lag forecasts.

**Controls:** non-negative finite amounts, required dimensions, explicit missing-day policy, chronological splits, deterministic seeds, and no future observed values in recursive predictions.

**Limitations:** no causal claims, no external drivers, no hierarchy reconciliation, no automatic drift monitoring. Real-data evaluation and university-specific dissertation work remain necessary. See `docs/METHODOLOGY.md`.''')
