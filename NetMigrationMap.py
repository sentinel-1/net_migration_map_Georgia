#!/usr/bin/env python
# coding: utf-8

# # Net Migration of Georgia
# 
# Purpose of this notebook is to create a choropleth world map reflecting a net migration of Georgia by citizenship over long period of time (period of time depends on the data available). Two different color scales are used, red and green, the red color scale is used for highlighting countries if the net migration in Georgia is a negative number for their citizens and the green color scale is used for highlighting countries if the net migration in Georgia is a positive number for their citizens.
# 
# 
# Four bars (like a sandwitch) are placed in the Black Sea near the Georgia on the map in order to reflect information about the data that is not associated with a citizenship of any particular country, such as:
# - **Stateless** bar: Shows net migration of stateless persons who do not have citizenship of any country.
# - **Not stated** bar: Shows net migration of persons whos citizenship is not indicated in the data.
# - **Other** bar: Shows net migration of persons who were identified as citizens of some particular country other than the ones listed by the Geostat in the published data.
# - **Total** bar: Shows total net migration of Georgia over the given period of time which include all the migrants regardless of citizenship.
# 
# *Tip: Hover the bars or different countries in the given choropleth map with your mouse in order to get a tooltip showing the relevant details.*
# 
# 
# 
# 
# Definitions:
#  - **Immigrant** (as defined by the Geostat for the data used here) – "a person recorded when crossing the National border i) who entered the country and has cumulated a
#    minimum of 183 days of residence in the country during the twelve following months; and ii) who was not usual
#    resident of the country when entering the country which means that he spent at least a cumulate duration of 183 days
#    of residence outside the country during the twelve months before entering the country."
#  - **Emigrant** (as defined by the Geostat for the data used here) – "a person recorded when crossing the National border and i) who crossed the border and left the country
#    and has cumulated a minimum of 183 days of residence outside the country during the twelve following months; and
#    ii) who was usual resident of the country when leaving the country which means that he spent at least a cumulate
#    duration of 183 days of residence inside the country during the twelve months before leaving the country."
#  - **Net migration** (as used in this notebook) – a difference between the number of immigrants and the number of emigrants during the given interval of time.
# 
# 
# 
# Data sources:
# - Statistical data of the Number of immigrants and emigrants of Georgia by sex and citizenship (in Excel format) is retrieved on Jun 9, 2022 from the website of the National Statistics Office of Georgia (Geostat): [geostat.ge](https://www.geostat.ge/en/)
# 
# - Statistical data of the Number of immigrants and emigrants of Georgia by sex and citizenship (in CSV format) is retrieved on Jun 11, 2022 from the "Statistics Database" website of the National Statistics Office of Georgia (Geostat): [pc-axis.geostat.ge](http://pc-axis.geostat.ge/PXWeb/pxweb/en/Database/)
# - Metadata (in PDF format) for the given statistical data is retrieved on Jun 14, 2022 from the website of the National Statistics Office of Georgia (Geostat): [geostat.ge](https://www.geostat.ge/en/)
# - Map data of the borders of the countries *(1:10m Cultural Vectors - Admin 0 – Countries - (latest) version 5.1.1)* is retrieved on Jun 11, 2022 from the "Natural Earth" website: [naturalearthdata.com](https://www.naturalearthdata.com/)
# 
# 

# In[1]:


from datetime import datetime, timedelta
nb_st = datetime.utcnow()
print(f"\nNotebook START time: {nb_st} UTC\n")


# In[2]:


get_ipython().run_cell_magic('HTML', '', '<script>\n  function code_toggle() {\n    if (code_shown) {\n      $(\'div.input\').hide(\'500\');\n      $(\'#toggleButton\').val(\'Show Python Code\')\n    } else {\n      $(\'div.input\').show(\'500\');\n      $(\'#toggleButton\').val(\'Hide Python Code\')\n    }\n    code_shown = !code_shown\n  }\n\n  $( document ).ready(function(){\n    code_shown=false;\n    $(\'div.input\').hide();\n    $(\'div.input:contains("%%HTML")\').removeClass( "input")\n  });\n</script>\n<form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Python Code"></form>\n')


# In[3]:


import numpy as np
import pandas as pd
from IPython.display import display
import geopandas
import warnings
import io
import json
import folium


# In[4]:


VERBOSE = False


# In[5]:


migration_df = pd.read_csv("data/geostat/EN/CSV/Migration.csv", skiprows=2, index_col="citizenship").head(-2).astype(int)

migration_df = migration_df.T.assign(
    Year=lambda df:pd.Series([str(x).strip().split()[0] for x in df.index], index=df.index).astype(int),
    MigrantType=lambda df:pd.Series([str(x).strip().split()[1].strip() for x in df.index], index=df.index).replace({
        'Immigrants': 'Immigrant',
        'Emigrants': 'Emigrant'
    }).astype('category'),
    Sex=lambda df:pd.Series([str(x).strip().split()[-1].strip() for x in df.index], index=df.index).replace({
        'Males': 'Male',
        'Females': 'Female',
        'sexes': 'All'
    }).astype('category')
)

start_year, end_year = migration_df['Year'].min(), migration_df['Year'].max()

print("\nGiven migration data covers the interval of time"
      f" from {start_year}"
      f" to {end_year} (inclusive).\n")

if VERBOSE:
    display(migration_df)


# In[6]:


not_country_names = ('Stateless', 'Not stated', 'Other', 'Total',)

def calculate_net_migration_by_citizenship(df: pd.DataFrame, Sex: str='All') -> pd.DataFrame:
    assert Sex in df['Sex'].cat.categories, f'Data not found for the Sex="{Sex}" filter, available categories are: {", ".join(list(df["Sex"].cat.categories))}.'
    df = pd.DataFrame({
        'Immigrant': df.loc[(df['Sex'] == Sex) & (df['MigrantType'] == 'Immigrant'), df.columns.difference(['Year'])].sum(numeric_only=True),
        'Emigrant': df.loc[(df['Sex'] == Sex) & (df['MigrantType'] == 'Emigrant'), df.columns.difference(['Year'])].sum(numeric_only=True)
    })
    df = (df['Immigrant'] - df['Emigrant']).reset_index(name='NetMigration')
    df = pd.concat([
        df.loc[~df['citizenship'].isin(not_country_names)].sort_values(by='NetMigration', ascending=False),
        df.loc[df['citizenship'].isin(not_country_names)].sort_values(by='NetMigration', ascending=False)
    ]).reset_index(drop=True)
    return df


# In[7]:


net_migration = {}

for Sex in ("Female", "Male", "All"):
    net_migration[Sex] = calculate_net_migration_by_citizenship(migration_df, Sex=Sex)

    if VERBOSE:
        print(f"\n{start_year}-{end_year} Net Migration of Georgia by citizenship for sex=\"{Sex}\":\n")
        display(net_migration[Sex])


# In[8]:


if VERBOSE:
    
    for Sex in ("Female", "Male", "All"):
        print(f'\nDescriptive statistics of the full {start_year}-{end_year} Net Migration data for Sex="{Sex}":\n')
        display(net_migration[Sex].loc[net_migration[Sex]['citizenship'] != 'Total'].describe())
        print(f'\nDescriptive statistics of the positive values having identifiable citizenship from the {start_year}-{end_year} Net Migration data for Sex="{Sex}":\n')
        display(net_migration[Sex].loc[(net_migration[Sex]['NetMigration'] > 0) & (~net_migration[Sex]['citizenship'].isin(not_country_names)),'NetMigration'].describe())
        print(f'\nDescriptive statistics of the negative values having identifiable citizenship from the {start_year}-{end_year} Net Migration data for Sex="{Sex}":\n')
        display(net_migration[Sex].loc[(net_migration[Sex]['NetMigration'] < 0) & (~net_migration[Sex]['citizenship'].isin(not_country_names)),'NetMigration'].describe())
        print('\n\n\n')


# In[9]:


countries_geodf = geopandas.read_file('data/naturalearth/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')


# In[10]:


def number_of_mismatched_names(df: pd.DataFrame, geodf: pd.DataFrame=countries_geodf) -> int:
    mismatch = df.loc[(~df['citizenship'].isin(geodf['NAME'])) & (~df['citizenship'].isin(not_country_names)),'citizenship']
    N = len(mismatch)
    
    if VERBOSE:
        print(f'Number of mismatched names between map data and statistic data is: {N}')
    
        if N > 0:
            print(f'Mismatched names: {[name for name in mismatch]}')
    return N


# In[11]:


number_of_mismatched_names(net_migration["All"])
pass


# In[12]:


if VERBOSE:
    print("Searching for equivalents used by the map data for the mismatched names detected above: ")
    print(countries_geodf.loc[countries_geodf['NAME'].str.contains('Russ'),'NAME'])
    print(countries_geodf.loc[countries_geodf['NAME'].str.contains('Iran'),'NAME'])


# In[13]:


def fix_mismatched_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace({
        'Russian Federation': 'Russia',
        'Iran, Islamic Republic of': 'Iran',
    })

for Sex in ("Female", "Male", "All"):
    net_migration[Sex] = fix_mismatched_names(net_migration[Sex])
    
    if VERBOSE:
        print(f'Replaced mismatched names in the data for Sex="{Sex}":\n - ', end="")
    assert number_of_mismatched_names(net_migration[Sex]) == 0, "ERROR: Please resolve name mismatch first..."


# In[14]:


with io.BytesIO() as buffer:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        countries_geodf.to_file(buffer, driver='GeoJSON')
    countries_geojson = json.loads(buffer.getvalue().decode("utf-8"))

with open("black_sea_sandwitch.json") as f:
    sandwitch_geojson = json.load(f)

countries_geojson['features'] += sandwitch_geojson['features']


# In[15]:


import branca.colormap as cmp

min_value = min([net_migration[Sex]['NetMigration'].min() for Sex in ("Female", "Male", "All")])
max_value = max([net_migration[Sex]['NetMigration'].max() for Sex in ("Female", "Male", "All")])

linear_positive_color = cmp.LinearColormap(
    ['#ccffcd', 'green'],
    vmin=0, vmax=max_value,
    caption=f'Positive number color scale of {start_year}-{end_year} Net Migration of Georgia'
)

linear_negative_color = cmp.LinearColormap(
    ['red','#ffcccd'],
    vmin=min_value, vmax=0,
    caption=f'Negative number color scale of {start_year}-{end_year} Net Migration of Georgia'
)

def get_map_color(NAME:str, Sex:str) -> str:
    x = net_migration[Sex].loc[net_migration[Sex]['citizenship']==NAME,'NetMigration']
    
    if len(x) == 0:
        return '#000000'
    x = x.item()
    
    if x < 0:
        return linear_negative_color(x)
    return linear_positive_color(x)


if VERBOSE:
    print("Color scale for negative numbers:")
    display(linear_negative_color)
    print("Color scale for positive numbers:")
    display(linear_positive_color)


# In[16]:


def _num_to_str(n: int) -> str:
    return f"{'+' if n > 0 else ''}{n}"

def get_net_migration_tooltip_by_citizenship(citizenship: str) -> str:
    tooltip = f'&quot;{start_year}-{end_year} Net Migration of Georgia&quot;<br>'
    
    n_female, n_male,  n_all = [
        (lambda df:df.loc[df['citizenship']==citizenship, 'NetMigration'])(net_migration[Sex])
        for Sex in ("Female", "Male", "All")
    ]
    
    if citizenship in not_country_names:
        tooltip += {
            'Stateless': '<strong>Stateless persons</strong>',
            'Not stated': 'Citizenship <strong>not stated</strong>',
            'Other': '<strong>Other</strong> (citizenship not given)',
            'Total': '<strong>Total Net Migration of Georgia</strong>'
        }[citizenship]
    else:
        tooltip += f"Migrated citizens of <strong>{citizenship}</strong> in Georgia"
    tooltip += ': <br>'
    
    if len(n_all) == 0:
        tooltip += "Not given (included in \"Other\")"
    else:
        tooltip += f"<strong>{_num_to_str(n_all.item())}</strong> "
        n_male = n_male.item() if len(n_male) else 0
        n_female = n_female.item() if len(n_female) else 0
        
        if  abs(n_male) > abs(n_female):
            tooltip += f"(Male: {_num_to_str(n_male)}, Female: {_num_to_str(n_female)})"
        else:
            tooltip += f"(Female: {_num_to_str(n_female)}, Male: {_num_to_str(n_male)})"
    return tooltip


if VERBOSE:
    display(get_net_migration_tooltip_by_citizenship("Georgia"), get_net_migration_tooltip_by_citizenship("Antarctica"))


# In[17]:


tbilisi_coordinate = [41.69339329182433, 44.80151746492941]
m = folium.Map(location=tbilisi_coordinate, zoom_start=6)

linear_negative_color.add_to(m)
linear_positive_color.add_to(m)

Sex=(
    "Female",  # 0
    "Male",  # 1
    "All"  # 2
)[2]

geojson = countries_geojson.copy()
m_layer = folium.GeoJson(
    geojson,
    style_function=lambda feature: {
        'fillColor': get_map_color(feature['properties']['NAME'], Sex),
        'color': 'black',  # border color
        'weight': 1,  # border thikness
        # 'dashArray': '5, 3',  # dashed 'line length,space length'
        'fillOpacity': 0.7,
        'nanFillOpacity': 0.4,
        'lineOpacity': 0.2,
    },
    name='Net Migration of Georgia by citizenship' + (f' (Sex="{Sex}")' if Sex!="All" else ''),
    # zoom_on_click=True,
    # show=Sex=="All",
)

for feature in geojson['features']:
    feature['properties']['tooltip_msg'] = get_net_migration_tooltip_by_citizenship(feature['properties']['NAME'])
folium.GeoJsonTooltip(
    fields=["tooltip_msg"],
    labels=False
).add_to(m_layer)

for feature in sandwitch_geojson['features']:
    coord = feature['geometry']['coordinates'][0][3]
    folium.map.Marker(
        [coord[1], coord[0]],
        icon=folium.DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: inherit; color:#333333; white-space:nowrap;"><b>%s</b></div>' % feature['properties']['NAME'],
            class_name="div-icon-text"
        )
    ).add_to(m_layer)
m_layer.add_to(m)



m.get_root().html.add_child(folium.Element(f"""
<script type="text/javascript">
window.onload = ()=>{{
    let zoomText = ()=>{{
        $(".div-icon-text").css("font-size", (0.02*{m.get_name()}.getZoom()**2)+"em");
    }};
    zoomText();
    {m.get_name()}.on("zoomend", ()=>{{zoomText();}});
}};
</script>
"""))
folium.LayerControl().add_to(m)



display(m)


# In[18]:


print(f"\n ** Total Elapsed time: {datetime.utcnow() - nb_st} ** \n")
print(f"Notebook END time: {datetime.utcnow()} UTC\n")


# 
# *This notebook is originally published under the Apache License (Version 2.0) at the following GitHub repository: [sentinel-1/net_migration_map_Georgia](https://github.com/sentinel-1/net_migration_map_Georgia)*
# 
# For the issues, feedback or suggestions regarding the original notebook (if any) feel free to open an issue at the corresponding [Issues page of the repository](https://github.com/sentinel-1/net_migration_map_Georgia/issues)

# In[ ]:




