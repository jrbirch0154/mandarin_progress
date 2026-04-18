# Better Progress Tracker
# Fri Apr 17 23:41:13 2026
# Jacob Birch

#%% Initializing

import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

url = 'https://docs.google.com/spreadsheets/d/1PY62lSxcqybPLpl5-3YTh8Ab1udidVRrBhPIp3oJDqk/export?format=csv&gid=1033082167#gid=1033082167'

df = pd.read_csv(url)

target_min = 30

def color_picker(x):
    if x >= target_min:
        return 'blue'
    else:
        return 'red'


#%% DF Stuff
df['Date'] = pd.to_datetime(df['Date'])
df['Level'] = df['Level'].str.extract(r'(\d+\.?\d*)')
df['Level'] = pd.to_numeric(df['Level'])
df = df.dropna(subset='Input (Min)')
df['hit_target'] = df['Input (Min)'] >= target_min
df['color'] = df['Input (Min)'].apply(color_picker)
print(df.dtypes)



#%% Plot 1

fig = px.line(df,
              x='Date',
              y='Total (H)',
              title=('Mandarin Hours over Time'),
              template='presentation'
              
              
              
              )

fig.update_yaxes(range=[0, 100])
fig.update_traces(fill='tozeroy',fillcolor='rgba(99,110,250,.2)')
fig.add_hline(y=50, line_dash='dash',line_color='red',line_width=1)

fig.show()

#%% Plot 2
fig2 = px.bar(df,
              x='Date',
              y='Input (Min)',
              title=('Mandarin Minutes Per Day'),
              template='presentation',
              color='color',
              color_discrete_map={'blue': 'blue', 'red': 'red'}
              )
fig2.add_hline(y=30,line_dash='dash',line_color='red',line_width=1)
fig2.show()