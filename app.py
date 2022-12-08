import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import folium 
# from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import plotly.express as px
from rapidfuzz import process, fuzz
import ast

# from streamlit_extras.altex import bar_chart

def add_markers(df,lat,long,color,icon,basemap):
    df=df[df[lat]!='NA']
    df=df[df[long]!='NA']
    try:
        df=df[df["Neighborhood_Geopy"]!="No Details"]
    except:
        pass
    for i in range(0,len(df)):
        if color=="red":
            marker = folium.Marker(location=[df.iloc[i][lat], df.iloc[i][long]],
                            popup=df.iloc[i]["OFFENSE_DESCRIPTION"]+" at "+str(df.iloc[i]["STREET"]), 
                            icon = folium.Icon(icon_size=(27, 27),
                                                  color=color,
                                                  icon=icon,
                                                  prefix='fa'),
                                ).add_to(basemap)
        if color=="blue":
            marker = folium.Marker(location=[df.iloc[i][lat], df.iloc[i][long]],
                                popup=df.iloc[i]["Location"], 
                                icon = folium.Icon(icon_size=(27, 27),
                                                      color=color,
                                                      icon=icon,
                                                      prefix='fa'),
                                    ).add_to(basemap)
        if color=="orange":
            marker = folium.Marker(location=[df.iloc[i][lat], df.iloc[i][long]],
                                popup=str(df.iloc[i]["BusinessName"])+" at "+str(df.iloc[i]["Address"]), 
                                icon = folium.Icon(icon_size=(27, 27),
                                                      color=color,
                                                      icon=icon,
                                                      prefix='fa'),
                                    ).add_to(basemap)
        if color=="green":    		
            marker = folium.Marker(location=[df.iloc[i][lat], df.iloc[i][long]],
                                popup=df.iloc[i]["address"]+" at "+str(df.iloc[i]["price"])+" ("+str(int(df.iloc[i]["beds"]))+" bed\'"+","+str(df.iloc[i]["baths"])+" bath\'"+","+str(df.iloc[i]["area"])+")", 
                                icon = folium.Icon(icon_size=(27, 27),
                                                      color=color,
                                                      icon=icon,
                                                      prefix='fa'),
                                    ).add_to(basemap)
        if color=="darkpurple":
            marker = folium.Marker(location=[df.iloc[i][lat], df.iloc[i][long]],
                                popup=df.iloc[i]["University_Name"], 
                                icon = folium.Icon(icon_size=(42, 42),
                                                      color=color,
                                                      icon=icon,
                                                      prefix='fa'),
                                    ).add_to(basemap)
        if color=="black":
            marker = folium.Marker(location=[df.iloc[i][lat], df.iloc[i][long]],
                                popup=str(df.iloc[i]["BusinessName"])+" at "+str(df.iloc[i]["Address"]), 
                                icon = folium.Icon(icon_size=(100, 100),
                                                      color=color,
                                                    #   icon=icon,
                                                      prefix='fa'),
                                    ).add_to(basemap)
                        


st.set_page_config(
    page_title = 'OFF-Campus Housing',
    page_icon = '✅',
    layout = 'wide'
)

crimedf=pd.read_csv("Crime-Boston.csv")

hospital_df=pd.read_csv("Hospital-Boston.csv")

restaurant_df=pd.read_csv("Restaurants-Boston.csv")

zillow_df=pd.read_csv("Zillow-Boston.csv")

university_df=pd.read_csv("University_Locations.csv")

crimedff=pd.read_csv("Crime-Boston-full.csv")

hospital_dff=pd.read_csv("Hospital-Boston.csv")

restaurant_dff=pd.read_csv("Restaurants-Boston.csv")

zillow_dff=pd.read_csv("Zillow-Boston.csv")

basemap = folium.Map(location=[42.3601, -71.0589], tiles="Stamen Terrain", zoom_start=12)

basemap_crime = folium.Map(location=[42.3601, -71.0589], tiles="Stamen Terrain", zoom_start=12)

basemap_hospital= folium.Map(location=[42.3601, -71.0589], tiles="Stamen Terrain", zoom_start=12)

basemap_restaurant= folium.Map(location=[42.3601, -71.0589], tiles="Stamen Terrain", zoom_start=12)

# basemap_zillow = folium.Map(location=[42.3601, -71.0589], tiles="Stamen Terrain", zoom_start=12)


basemap_zillow_price = folium.Map(location=[42.3601, -71.0589],zoom_start=12)
basemap_crime_shooting = folium.Map(location=[42.3601, -71.0589],zoom_start=12)


st.title("Housing Recommendations")

university_list=["Northeastern University",\
 "UMass Boston","MIT","Harvard","Boston University","Wentworth Institute of Technology",\
 "Hult","Suffolk University","Bentley University","Tufts University"]
university_names = st.multiselect("Which University you go to?", (university_list),university_list[:5])
university_name_eval = ", ".join(university_names)



# housing_kind = st.selectbox("What kind of housing do you live in?",("On-Campus","Off-Campus"))

place_stay = st.multiselect("Where do you stay?",("South End","Downtown Boston","ChinaTown",\
    "Financial District","Beacon Hill","Back Bay","Fenway/Kenmore","Mission Hill","Jamaica Plain",
    "Forest Hills/Woodbourne","Roslindale","Mattapan","Hyde Park","Dorchester","Roxbury",\
    "East Boston","Allston","Chestnut Hill","North End","Cambridgeport","West End",\
    "South Boston","Brighton","Longwood Medical Area","Brookline","Watertown","Arlington",\
    "Malden","Medford","Cambridge","Charlestown","Somerville","Waltham"),["Mission Hill"])
place_stay_eval = ", ".join(place_stay)

# rent_pay = st.selectbox("How much rent do you pay per month for your spot [Excluding Utilities]?",\
#     ("$400-$500","$500-$600","$600-$700","$700-$800",">$800"))


# utilities_pay = st.selectbox("How much do you pay for utilities per month?",("0-$50","$50-$100",\
#     "$100-$150",">$150"))

# utililities_included_in_rent = st.selectbox("What utilities do you have included in your rent?",("Heat","Electricity",\
#     "Gas","Water","Heat & Electricty","Gas & Heat","All"))

# apartment_size = st.selectbox("How big is your apartment?",("3bed-2bath","2bed-2bath",\
#     "2bed-1bath","1bed-1bath","Others"))

# groceries_pay = st.selectbox("How much do you pay for groceries per month?",("$50-$75","$75-$125",\
#     ">$125"))

# share_apt = st.selectbox("How many people do you share your apartment with?",("Not Sharing","2",\
#     "3","4",">5"))

# private_room = st.selectbox("Do you have a private room?",("Yes","No"))

# house_kind = st.selectbox("What kind of house are you staying in?",("Condo","Townhouse","Apartment"))

ethnicity_list=["American","Indian","Chinese","Latino/Hispanic",\
    "Pakistani","African","Others"]
ethnicity = st.multiselect("What is your ethnicity?",(ethnicity_list),ethnicity_list)
ethnicity_eval = ", ".join(ethnicity)

# self_identify = st.selectbox("How do you self identify?",("Male","Female","Non-binary/third gender",\
#     "Prefer not to say"))

# mode_transport = st.selectbox("What mode of transport do you travel from?",("Orange Line","Red Line",\
#     "Green Line","Bus","Walk","Car","Bike"))

# far_from_uni = st.selectbox("How far do you stay from university?",("0-0.5 Miles","0.5-1 Miles",\
#     "1-1.5 Miles","1.5-2 Miles",">2 Miles"))

# shuttle = st.selectbox("Is your university's shuttle service (Eg: RedEye for Northeastern) accessible to you?",\
#     ("Yes","Maybe","No"))

# restaurant_scale = st.selectbox("On a scale of 1-5 , How important is it to have restaurants/bars around you?",\
#     ("1","2","3","4","5"))

restaurant = st.text_input("Name your favorite restaurant where you stay?")

restaurant_dff = restaurant_dff.astype({'BusinessName':'string'})

restaurant_choices=restaurant_dff["BusinessName"].tolist()

if restaurant:
    similar=process.extractOne(str(restaurant), restaurant_choices, scorer=fuzz.token_set_ratio)
    # print(similar[0])
    restaurant_dff_popup=restaurant_dff[restaurant_dff["BusinessName"]==str(similar[0])]

    add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap)

    add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap_crime)

    add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap_hospital)

    add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap_restaurant)

    # add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap_zillow)

    add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap_zillow_price)

    add_markers(restaurant_dff_popup,'Latitude','Longitude','black', 'cutlery',basemap_crime_shooting)



    # st.table(restaurant_dff_popup)

# grocery_number = st.selectbox("How many grocery stores are near you?",("1","2","3","4","5"))

if place_stay:
    st.header("Map From Boston-Data for "+str(place_stay_eval))
else:
    st.header("Map From Boston-Data")


## Visuals based on Place of Stay
crimedf=crimedf[crimedf["Neighborhood_Geopy"].isin(place_stay)]

hospital_df=hospital_df[hospital_df["Neighborhood_Geopy"].isin(place_stay)]

zillow_df=zillow_df[zillow_df["Neighborhood_Geopy"].isin(place_stay)]

restaurant_df=restaurant_df[restaurant_df["Neighborhood_Geopy"].isin(place_stay)]

add_markers(crimedf,'Lat','Long','red','exclamation-circle',basemap)

add_markers(hospital_df,'YCOORD','XCOORD','blue', 'stethoscope',basemap)

add_markers(restaurant_df,'Latitude','Longitude','orange', 'cutlery',basemap)

add_markers(zillow_df,'Lat','Long','green', 'building',basemap)

add_markers(university_df,'Lat','Long','darkpurple', 'university',basemap)


folium_static(basemap)

# For Crime Data
if place_stay:
    st.header("Crime Data for "+str(place_stay_eval))
else:
    st.header("Crime Data for Boston")


add_markers(university_df,'Lat','Long','darkpurple', 'university',basemap_crime)
add_markers(crimedf,'Lat','Long','red','exclamation-circle',basemap_crime)

folium_static(basemap_crime)

# For Hospital Data
if place_stay:
    st.header("Hospital Data for "+str(place_stay_eval))
else:
    st.header("Hospital Data for Boston")

add_markers(university_df,'Lat','Long','darkpurple', 'university',basemap_hospital)
add_markers(hospital_df,'YCOORD','XCOORD','blue', 'stethoscope',basemap_hospital)

folium_static(basemap_hospital)

# For Restaurant Data
if place_stay:
    st.header("Restaurant Data for "+str(place_stay_eval))
else:
    st.header("Restaurant Data for Boston")

add_markers(university_df,'Lat','Long','darkpurple', 'university',basemap_restaurant)
add_markers(restaurant_df,'Latitude','Longitude','orange', 'cutlery',basemap_restaurant)

folium_static(basemap_restaurant)

# For Zillow Price Data
if place_stay:
    st.header("Zillow Price Data for "+str(place_stay_eval))
else:
    st.header("Zillow Price Data for")

heat_data = zillow_df.groupby(["Lat","Long"])['pricem'].mean().reset_index().values.tolist()

add_markers(university_df,'Lat','Long','darkpurple', 'university',basemap_zillow_price)
add_markers(zillow_df,'Lat','Long','green','building',basemap_zillow_price)

HeatMap(heat_data).add_to(basemap_zillow_price)
folium_static(basemap_zillow_price)

# For Crime Shooting Data
if place_stay:
    st.header("Crime Shooting Data for "+str(place_stay_eval))
else:
    st.header("Crime Shooting Data")

heat_data_crime = crimedf.groupby(["Lat","Long"])['SHOOTING'].mean().reset_index().values.tolist()

add_markers(university_df,'Lat','Long','darkpurple', 'university',basemap_crime_shooting)
add_markers(crimedf,'Lat','Long','red','exclamation-circle',basemap_crime_shooting)

HeatMap(heat_data_crime).add_to(basemap_crime_shooting)
folium_static(basemap_crime_shooting)


# st.bar_chart()

if place_stay:
    st.header("Crime Shooting Data for "+str(place_stay_eval))
else:
    st.header("Crime Shooting Data")

crime_count = crimedf["OFFENSE_DESCRIPTION"].value_counts(dropna=True, sort=True)
crime_count = crime_count[:10,]

df_crime_counts = pd.DataFrame(crime_count)
df_crime_counts_reset = df_crime_counts.reset_index()
df_crime_counts_reset.columns = ['crime_types', 'counts']
df_crime_counts_reset=df_crime_counts_reset.sort_values(["counts"],ascending=False)
fig = px.bar(df_crime_counts_reset,x='crime_types',y='counts')
st.plotly_chart(fig, use_container_width=True)
# bar_chart(data=df_crime_counts_reset,x="crime_types",y="counts")
st.table(df_crime_counts_reset)


dfc=crimedf.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Crime in Area').set_index("Neighborhood_Geopy")

dfh=hospital_df.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Hospitals in Area').set_index("Neighborhood_Geopy")

dfr=restaurant_df.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Restaurants in Area').set_index("Neighborhood_Geopy")

dfz=zillow_df.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Zillow Properties in Area').set_index("Neighborhood_Geopy")

dfchrz=pd.concat([dfc,dfh,dfr,dfz],axis=1).fillna(0)
for col in ['Counts of Crime in Area', 'Counts of Hospitals in Area', 'Counts of Restaurants in Area', 'Counts of Zillow Properties in Area']:
    dfchrz[col] = dfchrz[col].astype('int')

st.header(str(place_stay_eval)+" Locality Information")
st.table(dfchrz)


dfc=crimedff.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Crime in Area').set_index("Neighborhood_Geopy")

dfh=hospital_dff.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Hospitals in Area').set_index("Neighborhood_Geopy")

dfr=restaurant_dff.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Restaurants in Area').set_index("Neighborhood_Geopy")

dfz=zillow_dff.groupby(['Neighborhood_Geopy']).size().reset_index(name='Counts of Zillow Properties in Area').set_index("Neighborhood_Geopy")

dfchrz=pd.concat([dfc,dfh,dfr,dfz],axis=1).fillna(0)
for col in ['Counts of Crime in Area', 'Counts of Hospitals in Area', 'Counts of Restaurants in Area', 'Counts of Zillow Properties in Area']:
    dfchrz[col] = dfchrz[col].astype('int')

dfchrz['percent of crime'] = (dfchrz['Counts of Crime in Area'] / 
                  dfchrz['Counts of Crime in Area'].sum()) * 100
dfchrz['percent of hospitals'] = (dfchrz['Counts of Hospitals in Area'] / 
                  dfchrz['Counts of Hospitals in Area'].sum()) * 100
dfchrz['percent of restaurants'] = (dfchrz['Counts of Restaurants in Area'] / 
                  dfchrz['Counts of Restaurants in Area'].sum()) * 100
dfchrz['percent of zillow properties'] = (dfchrz['Counts of Zillow Properties in Area'] / 
                  dfchrz['Counts of Zillow Properties in Area'].sum()) * 100

dfchrz['percent of crime']=round(dfchrz['percent of crime'],2).astype(str) + '%'
dfchrz['percent of hospitals']=round(dfchrz['percent of hospitals'],2).astype(str) + '%'
dfchrz['percent of restaurants']=round(dfchrz['percent of restaurants'],2).astype(str) + '%'
dfchrz['percent of zillow properties']=round(dfchrz['percent of zillow properties'],2).astype(str) + '%'


dfchrz=dfchrz[["Counts of Crime in Area","percent of crime",\
        "Counts of Hospitals in Area","percent of hospitals",\
        "Counts of Restaurants in Area","percent of restaurants",\
        "Counts of Zillow Properties in Area","percent of zillow properties"]]

dfchrz=dfchrz.sort_values("Counts of Crime in Area",ascending=False)

st.header("Boston's Neighborhood Information")
st.table(dfchrz)

## Whole Dataset check


if restaurant:
    st.header("Most Similar Restaurant Name")
    similar=process.extractOne(str(restaurant), restaurant_choices, scorer=fuzz.token_set_ratio)
    # print(similar[0])
    st.table(restaurant_dff[restaurant_dff["BusinessName"]==str(similar[0])])


och=pd.read_excel("Project_DataSet.xlsx")

och=och.iloc[:,17:]
och.columns = och.iloc[0]

och=och.rename(columns=och.iloc[0])
och=och.drop(och.index[[0,1]])
och.reset_index(drop=True,inplace=True)


och=och[och["Which University you go to?"].isin(university_names)]

university_count  = och["Which University you go to?"].value_counts(dropna=True, sort=True)
# university_count = university_count[:10,]


st.header("Survey Data")

if place_stay:
    st.header("University Survey Data for "+str(university_name_eval))
else:
    st.header("University Survey Data")

df_university_counts = pd.DataFrame(university_count)
df_university_counts_reset = df_university_counts.reset_index()
df_university_counts_reset.columns = ['University', 'counts']
df_university_counts_reset=df_university_counts_reset.sort_values(["counts"],ascending=False)
fig = px.bar(df_university_counts_reset,x='University',y='counts')
st.plotly_chart(fig, use_container_width=True)
# bar_chart(data=df_university_counts_reset,x="University",y="counts")


och=och[och["What is your ethnicity? - Selected Choice"].isin(ethnicity)]

ethnicity_count  = och["What is your ethnicity? - Selected Choice"].value_counts(dropna=True, sort=True)
ethnicity_count = ethnicity_count[:10,]

st.header("Ethnicities from Survey")
df_ethnicity_counts = pd.DataFrame(ethnicity_count)
df_ethnicity_counts_reset = df_ethnicity_counts.reset_index()
df_ethnicity_counts_reset.columns = ['Ethnicity', 'counts']
df_ethnicity_counts_reset=df_ethnicity_counts_reset.sort_values(["counts"],ascending=False)
fig = px.bar(df_ethnicity_counts_reset,x='Ethnicity',y='counts')
st.plotly_chart(fig, use_container_width=True)

