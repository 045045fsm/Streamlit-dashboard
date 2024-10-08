# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EK9witwehm3oR0zyaroO4KBi_QGsvFhp
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
file_path = 'fifa_data.csv'  # Update with the correct file path
df = pd.read_csv(file_path, low_memory=False)

# Set the title of the Streamlit app
st.title('Football Players Dataset Explorer')

# Display the first few rows of the dataset
st.header('Dataset Overview')
st.dataframe(df.head())

# Adding Slicers
st.sidebar.header("Filter Players")
selected_club = st.sidebar.multiselect("Select Club", options=df['club_name'].unique(), default=[])
selected_nationality = st.sidebar.multiselect("Select Nationality", options=df['nationality_name'].unique(), default=[])
selected_position = st.sidebar.multiselect("Select Position", options=df['player_positions'].unique(), default=[])
selected_age = st.sidebar.slider("Select Age Range", min_value=int(df['age'].min()), max_value=int(df['age'].max()), value=(int(df['age'].min() + df['age'].max())//2, int(df['age'].min() + df['age'].max())//2))

# Applying Filters
filtered_df = df[
    (df['club_name'].isin(selected_club) if selected_club else True) &
    (df['nationality_name'].isin(selected_nationality) if selected_nationality else True) &
    (df['player_positions'].isin(selected_position) if selected_position else True) &
    (df['age'].between(selected_age[0], selected_age[1]))
]

# Convert necessary columns to numeric types, handling errors if necessary
numeric_columns = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'attacking_heading_accuracy', 'height_cm']
filtered_df[numeric_columns] = filtered_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values in the selected columns for the scatter matrix plot
scatter_matrix_df = filtered_df[numeric_columns].dropna()

# 1. Does the Age of the Player Affect Ball Control Performance?
st.header('1. Age vs. Ball Control Performance')
age_ball_control_fig = px.scatter(filtered_df, x='age', y='skill_ball_control', trendline="ols",
                                  title="Age vs. Ball Control",
                                  labels={'age': 'Age of Player', 'skill_ball_control': 'Ball Control Skill'})
st.plotly_chart(age_ball_control_fig)

# 2. Show how Height affects different factors like Stamina, Dribbling, Pace, Passing, and Heading Accuracy
st.header('2. Height vs. Performance Metrics')
height_metrics_fig = go.Figure()
height_metrics_fig.add_trace(go.Scatter(x=filtered_df['height_cm'], y=filtered_df['power_stamina'], mode='markers', name='Stamina'))
height_metrics_fig.add_trace(go.Scatter(x=filtered_df['height_cm'], y=filtered_df['dribbling'], mode='markers', name='Dribbling'))
height_metrics_fig.add_trace(go.Scatter(x=filtered_df['height_cm'], y=filtered_df['pace'], mode='markers', name='Pace'))
height_metrics_fig.add_trace(go.Scatter(x=filtered_df['height_cm'], y=filtered_df['passing'], mode='markers', name='Passing'))
height_metrics_fig.add_trace(go.Scatter(x=filtered_df['height_cm'], y=filtered_df['attacking_heading_accuracy'], mode='markers', name='Heading Accuracy'))
height_metrics_fig.update_layout(title="Height vs. Stamina, Dribbling, Pace, Passing, and Heading Accuracy",
                                 xaxis_title="Height (cm)", yaxis_title="Performance Metrics")
st.plotly_chart(height_metrics_fig)

# 3. Show if there is a relation between Wage and Overall of the Players
st.header('3. Wage vs. Overall Rating')
wage_overall_fig = px.scatter(filtered_df, x='wage_eur', y='overall', trendline="ols",
                              title="Wage vs. Overall Rating",
                              labels={'wage_eur': 'Wage (EUR)', 'overall': 'Overall Rating'})
st.plotly_chart(wage_overall_fig)

# 4. Show the Top Quickest Players
st.header('4. Top Quickest Players')
top_quickest = filtered_df.nlargest(10, 'pace')[['short_name', 'pace', 'club_name']]
quickest_fig = px.bar(top_quickest, x='short_name', y='pace', color='club_name', title="Top Quickest Players")
st.plotly_chart(quickest_fig)

# 5. Determine if there is a relation between the Position of the Player and his Wage and Value
st.header('5. Position vs. Wage and Value')
position_wage_value_fig = px.scatter(filtered_df, x='wage_eur', y='value_eur', color='player_positions',
                                     title="Position vs. Wage and Value",
                                     labels={'wage_eur': 'Wage (EUR)', 'value_eur': 'Value (EUR)'})
st.plotly_chart(position_wage_value_fig)

# 6. See the Nationality of the Players that got the highest Wages
st.header('6. Nationalities with the Highest Wages')
nationality_wages_fig = px.box(filtered_df, x='nationality_name', y='wage_eur', points="all", title="Nationalities with the Highest Wages",
                               labels={'nationality_name': 'Nationality', 'wage_eur': 'Wage (EUR)'})
nationality_wages_fig.update_xaxes(type='category')
st.plotly_chart(nationality_wages_fig)

# 7. Show the effect of Age on the Potential of the Players
st.header('7. Age vs. Overall Rating')
age_overall_fig = px.scatter(filtered_df, x='age', y='overall', trendline="ols", title="Age vs. Overall Rating",
                               labels={'age': 'Age of Player', 'overall': 'Overall Rating'})
st.plotly_chart(age_overall_fig)


# 8. View the Top 50 Players and their Clubs
st.header('8. Top 50 Players and their Clubs')
top_50_players = filtered_df.nlargest(50, 'overall')[['short_name', 'overall', 'club_name', 'nationality_name']]
top_50_fig = px.bar(top_50_players, x='short_name', y='overall', color='club_name', title="Top 50 Players and their Clubs")
st.plotly_chart(top_50_fig)

# Footer
st.text('Streamlit app by Rishi Goswami')