#!/usr/bin/env python
# coding: utf-8

# ## Net Migration Map of Georgia by Citizenship
# 
# *Tip: Hover the bars or different countries in the given choropleth map with your mouse in order to get a tooltip showing the relevant details.*
# 
# 

# In[1]:


from IPython.display import display, HTML, IFrame, Javascript
display(HTML("""
<style>
.net-migration-map-cell {
  padding: 0 !important;
  width: calc(100% + 30px) !important;
  margin-left: -15px !important;
}

.net-migration-map-cell .map-wrapper {
  padding: 0;
  margin: 0;
  width: 100%;
  max-width: 100%;
}

.prompt {
  min-width: 12ex;
}

.net-migration-map-cell >*:not(.map-wrapper) {
  padding: 5px;
  margin-left: calc(15px + 12ex);
  margin-right: 15px;
}

.net-migration-map-cell .prompt,
.net-migration-map-cell div[class$="-prompt"] {
  display: none;
  margin-right: 15px;
}

.loader {
  border: 12px solid #f3f3f3;
  border-radius: 50%;
  border-top: 12px solid #adcaa1;
  width: 86px;
  height: 86px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 2s linear infinite;
  position: absolute;
  left: 50%;
  margin-left: -43px;
  top: 50%;
  margin-top: -43px;
  z-index: 1000;
}

/* Safari */
@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
"""))

map_html = HTML(
    '<div style="position:relative;width:100%;height:0;padding-bottom:60%;"'
    '  id="net-migration-map-container" >'
    '<div class="loader" id="net-migration-map-spinner"></div>'
)
map_html.data += IFrame(src="map.html", width='100%', height='100%', extras=[
    'style="position:absolute;width:100%;height:100%;left:0;top:0;'
    'border:none !important;"', 'allowfullscreen',
    """onload="javascript:setTimeout(()=>{document.getElementById("""
    """'net-migration-map-spinner').style.display='none';}, 2000)" """
])._repr_html_() + '</div>'
display(map_html)
display(Javascript("""
((fn)=>{
  if (document.readyState != 'loading') {
    fn();
} else {
    document.addEventListener('DOMContentLoaded', fn);
}
})(()=>{
let map_container = document.getElementById("net-migration-map-container");
let cell = map_container.parentNode;
while (cell.parentNode !== null
       && !cell.classList.contains("cell")
       && !cell.classList.contains("jp-Cell-outputArea")) {
  cell.classList.add("map-wrapper");
  cell = cell.parentNode;
}
cell.classList.add("net-migration-map-cell");
});
"""))


# \* Four bars (like a sandwitch) are placed in the Black Sea near the Georgia on the map above in order to reflect information about the data that is not associated with a citizenship of any particular country, such as:
# - **Stateless** bar: Shows net migration of stateless persons who do not have citizenship of any country.
# - **Not stated** bar: Shows net migration of persons whos citizenship is not stated in the data.
# - **Other** bar: Shows net migration of persons who were identified as citizens of some particular country other than the ones listed by the Geostat in the published data.
# - **Total** bar: Shows total net migration of Georgia over the given period of time which include all the migrants regardless of citizenship.

# 
# # Net Migration of Georgia
# 
# Purpose of this notebook is to create a choropleth world map reflecting a net migration of Georgia by citizenship over long period of time (period of time depends on the data available). The resulting map is displayed above. Two different color scales are used, red and green, the red color scale is used for highlighting countries if the net migration in Georgia is a negative number for their respective citizens and the green color scale is used in a same way but for positive numbers. Color (red/green) and the color intensity are assigned automatically based on the relevant statistics.
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

# In[2]:


from datetime import datetime, timedelta
nb_st = datetime.utcnow()
print(f"\nNotebook START time: {nb_st} UTC\n")


# In[3]:


get_ipython().run_cell_magic('HTML', '', '<style>\n@media (max-width: 540px) {\n  .output .output_subarea {\n    max-width: 100%;\n  }\n}\n</style>\n<script>\n  function code_toggle() {\n    if (code_shown){\n      $(\'div.input\').hide(\'500\');\n      $(\'#toggleButton\').val(\'🔎 Show Python Code\')\n    } else {\n      $(\'div.input\').show(\'500\');\n      $(\'#toggleButton\').val(\'⌦ Hide Python Code\')\n    }\n    code_shown = !code_shown\n  }\n\n  $( document ).ready(function(){\n    code_shown=false;\n    $(\'div.input\').hide();\n    $(\'div.input:contains("%%HTML")\').removeClass( "input")\n    $(\'div.input:contains("%%capture")\').removeClass("input")\n  });\n</script>\n<form action="javascript:code_toggle()">\n  <input type="submit" id="toggleButton" value="🔎 Show Python Code"\n         class="btn btn-default btn-lg">\n</form>\n')


# In[4]:


import numpy as np
import pandas as pd
import geopandas
import warnings
import io
import json
import folium
import branca.colormap as cmp
from folium.plugins import Fullscreen
from folium.utilities import normalize


# In[5]:


VERBOSE = False


# In[6]:


migration_df = pd.read_csv(
    "data/geostat/EN/CSV/Migration.csv",
    skiprows=2,
    index_col="citizenship"
).head(-2).astype(int)

migration_df = migration_df.T.assign(
    Year=lambda df: pd.Series(
        [
            str(x).strip().split()[0]
            for x in df.index
        ],
        index=df.index
    ).astype(int),
    MigrantType=lambda df: pd.Series(
        [
            str(x).strip().split()[1].strip()
            for x in df.index
        ],
        index=df.index
    ).replace({
        'Immigrants': 'Immigrant',
        'Emigrants': 'Emigrant'
    }).astype('category'),
    Sex=lambda df: pd.Series(
        [
            str(x).strip().split()[-1].strip()
            for x in df.index
        ],
        index=df.index
    ).replace({
        'Males': 'Male',
        'Females': 'Female',
        'sexes': 'All'
    }).astype('category')
)

start_year, end_year = migration_df['Year'].min(), migration_df['Year'].max()

print("\nGiven migration data covers the interval of time"
      f" from {start_year} to {end_year} (inclusive).\n")

if VERBOSE:
    display(migration_df)


# In[7]:


NOT_COUNTRY_NAMES = ('Stateless', 'Not stated', 'Other', 'Total',)

def get_net_migration_by_citizenship_df(df: pd.DataFrame,
                                        Sex: str = 'All') -> pd.DataFrame:
    assert Sex in df['Sex'].cat.categories, (
        'Data not found for the Sex="{Sex}" filter, available categories are: '
        f'{", ".join(list(df["Sex"].cat.categories))}.')
    df = pd.DataFrame({
        'Immigrant': df.loc[
            (df['Sex'] == Sex) & (df['MigrantType'] == 'Immigrant'),
            df.columns.difference(['Year'])
        ].sum(numeric_only=True),
        'Emigrant': df.loc[
            (df['Sex'] == Sex) & (df['MigrantType'] == 'Emigrant'),
            df.columns.difference(['Year'])
        ].sum(numeric_only=True)
    })
    df = (df['Immigrant'] - df['Emigrant']).reset_index(name='NetMigration')
    df = pd.concat([
        df.loc[
            ~df['citizenship'].isin(NOT_COUNTRY_NAMES)
        ].sort_values(by='NetMigration', ascending=False),
        df.loc[
            df['citizenship'].isin(NOT_COUNTRY_NAMES)
        ].sort_values(by='NetMigration', ascending=False)
    ]).reset_index(drop=True)
    return df


# In[8]:


net_migration = {}

for Sex in ("Female", "Male", "All"):
    net_migration[Sex] = get_net_migration_by_citizenship_df(migration_df,
                                                             Sex=Sex)

    if VERBOSE:
        print(f"\n{start_year}-{end_year} Net Migration of Georgia "
              f"by citizenship for sex=\"{Sex}\":\n")
        display(net_migration[Sex])


# In[9]:


if VERBOSE:
    
    for Sex in ("Female", "Male", "All"):
        print('\nDescriptive statistics of the '
              f'full {start_year}-{end_year} '
              f'Net Migration data for Sex="{Sex}":\n')
        display(
            net_migration[Sex].loc[
                net_migration[Sex]['citizenship'] != 'Total'
            ].describe()
        )
        print('\nDescriptive statistics of the positive values '
              'having identifiable citizenship '
              f'from the {start_year}-{end_year} Net Migration data '
              f'for Sex="{Sex}":\n')
        display(
            net_migration[Sex].loc[
                (net_migration[Sex]['NetMigration'] > 0) & 
                (~net_migration[Sex]['citizenship'].isin(NOT_COUNTRY_NAMES)),
                'NetMigration'
            ].describe()
        )
        print('\nDescriptive statistics of the negative values '
              'having identifiable citizenship '
              f'from the {start_year}-{end_year} Net Migration data '
              f'for Sex="{Sex}":\n')
        display(
            net_migration[Sex].loc[
                (net_migration[Sex]['NetMigration'] < 0) &
                (~net_migration[Sex]['citizenship'].isin(NOT_COUNTRY_NAMES)),
                'NetMigration'
            ].describe()
        )
        print('\n\n\n')


# In[10]:


countries_geodf = geopandas.read_file(
    'data/naturalearth/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp'
)


# In[11]:


def number_of_mismatched_names(
        df: pd.DataFrame,
        geodf: geopandas.GeoDataFrame = countries_geodf) -> int:
    mismatch = df.loc[
        (~df['citizenship'].isin(geodf['NAME'])) &
        (~df['citizenship'].isin(NOT_COUNTRY_NAMES)),
        'citizenship'
    ]
    N = len(mismatch)
    
    if VERBOSE:
        print('Number of mismatched names between map data and '
              f'statistic data is: {N}')
    
        if N > 0:
            print(f'Mismatched names: {[name for name in mismatch]}')
    return N


# In[12]:


number_of_mismatched_names(net_migration["All"])
pass


# In[13]:


def search_in_countries_geodf(substring: str) -> pd.Series:
    return countries_geodf.loc[countries_geodf['NAME'].str.contains(substring),
                               'NAME']

if VERBOSE:
    print("Searching for equivalents used by the map data "
          "for the mismatched names detected above: ")
    print(search_in_countries_geodf('Russ'))
    print(search_in_countries_geodf('Iran'))


# In[14]:


def fix_mismatched_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace({
        'Russian Federation': 'Russia',
        'Iran, Islamic Republic of': 'Iran',
    })


for Sex in ("Female", "Male", "All"):
    net_migration[Sex] = fix_mismatched_names(net_migration[Sex])
    
    if VERBOSE:
        print('Replaced mismatched names in the data '
              f'for Sex="{Sex}":\n - ', end="")
    assert number_of_mismatched_names(net_migration[Sex]) == 0, "ERROR:\
 Please resolve name mismatch first..."


# In[15]:


with io.BytesIO() as buffer:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        countries_geodf.to_file(buffer, driver='GeoJSON')
    countries_geojson = json.loads(buffer.getvalue().decode("utf-8"))

with open("black_sea_sandwitch.json") as f:
    sandwitch_geojson = json.load(f)

countries_geojson['features'] += sandwitch_geojson['features']


# In[16]:


min_value = min([net_migration[Sex]['NetMigration'].min()
                 for Sex in ("Female", "Male", "All")])

max_value = max([net_migration[Sex]['NetMigration'].max()
                 for Sex in ("Female", "Male", "All")])

color_scale = cmp.LinearColormap(
    ['red', '#ffcccd', '#ccffcd', 'green'],
    index=[min_value, 0, 0, max_value],
    vmin=min_value, vmax=max_value,
    # caption=f'{start_year}-{end_year} Net Migration of Georgia by Citizenship'
)


def get_map_color(NAME: str, Sex: str) -> str:
    x = net_migration[Sex].loc[net_migration[Sex]['citizenship']==NAME,
                               'NetMigration']
    return color_scale(x.item()) if len(x) else '#000000'


if VERBOSE:
    print("Color scale:")
    display(color_scale)


# In[17]:


def get_net_migration_tooltip_by_citizenship(citizenship: str) -> str:
    tooltip = (f'&quot;{start_year}-{end_year} '
               'Net Migration of Georgia&quot;<br>')
    
    n_female, n_male,  n_all = [
        (lambda df: df.loc[df['citizenship']==citizenship,
                           'NetMigration'])(
            net_migration[Sex])
        for Sex in ("Female", "Male", "All")
    ]
    
    if citizenship in NOT_COUNTRY_NAMES:
        tooltip += {
            'Stateless': '<strong>Stateless persons</strong>',
            'Not stated': 'Citizenship <strong>not stated</strong>',
            'Other': '<strong>Other</strong> (citizenship not given)',
            'Total': '<strong>Total Net Migration of Georgia</strong>',
        }[citizenship]
    else:
        tooltip += ("Migrated citizens of "
                    f"<strong>{citizenship}</strong> in Georgia")
    tooltip += ': <br>'
    
    if len(n_all) == 0:
        tooltip += "Not given (included in \"Other\")"
    else:
        tooltip += f"<strong>{n_all.item():+}</strong> "
        n_male = n_male.item() if len(n_male) else 0
        n_female = n_female.item() if len(n_female) else 0
        
        if abs(n_male) > abs(n_female):
            tooltip += f"(Male: {n_male:+}, Female: {n_female:+})"
        else:
            tooltip += f"(Female: {n_female:+}, Male: {n_male:+})"
    return tooltip


if VERBOSE:
    print("\nExamples of tooltips:\n")
    display(HTML("<p>{}</p><p>{}</p><br>".format(
        get_net_migration_tooltip_by_citizenship("Georgia"),
        get_net_migration_tooltip_by_citizenship("Antarctica"))))


# In[18]:


tbilisi_coordinate = [41.69339329182433, 44.80151746492941]
m = folium.Map(location=tbilisi_coordinate,
               zoom_start=6, scrollWheelZoom=False)

color_scale.add_to(m)

Sex = (
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
    name='Net Migration of Georgia by citizenship' + (
        f' (Sex="{Sex}")' if Sex!="All" else ''
    ),
    # zoom_on_click=True,
    # show=Sex=="All",
)

for feature in geojson['features']:
    feature['properties'][
        'tooltip_msg'
    ] = get_net_migration_tooltip_by_citizenship(feature['properties']['NAME'])
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
            html=('<div style="font-size: inherit; color:#333333; '
                  'white-space:nowrap;"><b>{:s}</b></div>').format(
                      feature['properties']['NAME']),
            class_name="div-icon-text"
        )
    ).add_to(m_layer)
m_layer.add_to(m)



m.get_root().html.add_child(folium.Element("""
<style>
@media (max-width: 500px) {
    .leaflet-right .legend {
        visibility: hidden;
    }
}
@media (max-width: 288px) {
    .leaflet-right {
        display: none;
    }
}
</style>
"""))
m.get_root().html.add_child(folium.Element(f"""
<script type="text/javascript">
window.onload = () => {{
    let zoomText = () => {{
        $(".div-icon-text")
            .css("font-size", (0.02 * {m.get_name()}.getZoom()**2) + "em");
    }};
    zoomText();
    {m.get_name()}.on("zoomend", () => {{zoomText();}});
    {m.get_name()}.on('click',
                      () => {{ {m.get_name()}.scrollWheelZoom.enable(); }});
    {m.get_name()}.on('mouseout',
                      () => {{ {m.get_name()}.scrollWheelZoom.disable(); }});
    {m.get_name()}.on('blur',
                      () => {{ {m.get_name()}.scrollWheelZoom.disable(); }});
}};
</script>
"""))
folium.LayerControl().add_to(m)
Fullscreen().add_to(m)


# display(m)
pass


# In[19]:


##
# Instead of displaying here save the map as static `map.html` file
# in order to display in the beggining of this notebook.
# FIXME: This approach may require 2x run of notebook to update the map
##
m.save("map.html")


# In[20]:


print(f"\n ** Total Elapsed time: {datetime.utcnow() - nb_st} ** \n")
print(f"Notebook END time: {datetime.utcnow()} UTC\n")


# In[21]:


get_ipython().run_cell_magic('capture', '', '%mkdir OGP_classic\n')


# In[22]:


get_ipython().run_cell_magic('capture', '', '%%file "OGP_classic/conf.json"\n{\n  "base_template": "classic",\n  "preprocessors": {\n    "500-metadata": {\n      "type": "nbconvert.preprocessors.ClearMetadataPreprocessor",\n      "enabled": true,\n      "clear_notebook_metadata": true,\n      "clear_cell_metadata": true\n    },\n    "900-files": {\n      "type": "nbconvert.preprocessors.ExtractOutputPreprocessor",\n      "enabled": true\n    }\n  }\n}\n')


# In[23]:


get_ipython().run_cell_magic('capture', '', '%%file "OGP_classic/index.html.j2"\n{%- extends \'classic/index.html.j2\' -%}\n{%- block html_head -%}\n\n{#  OGP attributes for shareability #}\n<meta property="og:url"          content="https://sentinel-1.github.io/net_migration_map_Georgia/" />\n<meta property="og:type"         content="article" />\n<meta property="og:title"        content="Net Migration Map of Georgia" />\n<meta property="og:description"  content="Choropleth Map of the Net Migration of Georgia by Citizenship" />\n<meta property="og:image"        content="https://raw.githubusercontent.com/sentinel-1/net_migration_map_Georgia/master/screenshots/2022-06-28_(1200x628).png" />\n<meta property="og:image:alt"    content="Screen Shot of the resulting map" />\n<meta property="og:image:type"   content="image/png" />\n<meta property="og:image:width"  content="1200" />\n<meta property="og:image:height" content="628" />\n    \n<meta property="article:published_time" content="2022-06-14T10:55:04+00:00" />\n<meta property="article:modified_time"  content="{{ resources.iso8610_datetime_utcnow }}" />\n<meta property="article:publisher"      content="https://sentinel-1.github.io" />\n<meta property="article:author"         content="https://github.com/sentinel-1" />\n<meta property="article:section"        content="datascience" />\n<meta property="article:tag"            content="datascience" />\n<meta property="article:tag"            content="geospatialdata" />\n<meta property="article:tag"            content="Python" />\n<meta property="article:tag"            content="data" />\n<meta property="article:tag"            content="analytics" />\n<meta property="article:tag"            content="datavisualization" />\n<meta property="article:tag"            content="bigdataunit" />\n<meta property="article:tag"            content="visualization" />\n<meta property="article:tag"            content="migration" />\n<meta property="article:tag"            content="Georgia" />\n    \n    \n{{ super() }}\n\n{%- endblock html_head -%}\n    \n    \n{% block body_header %}\n<body>\n    \n<div class="container">\n  <nav class="navbar navbar-default">\n    <div class="container-fluid">\n      <ul class="nav nav-pills  navbar-left">\n        <li role="presentation">\n          <a href="/">\n            <svg xmlns="http://www.w3.org/2000/svg"\n                 viewBox="0 0 576 512" width="1em">\n              <path \n                fill="#999999"\nd="M 288,0 574,288 511,288 511,511 352,511 352,352 223,352 223,511 62,511 64,288 0,288 Z"\n              />\n            </svg> Home\n          </a>\n        </li>\n      </ul>\n      <ul class="nav nav-pills  navbar-right">\n        <li role="presentation" class="active">\n          <a href="/net_migration_map_Georgia/">🇬🇧 English </a>\n        </li>\n        <li role="presentation">\n          <a href="/net_migration_map_Georgia/ka/">🇬🇪 ქართული</a>\n        </li>\n      </ul>\n    </div>\n  </nav>\n</div>\n\n\n\n  <div tabindex="-1" id="notebook" class="border-box-sizing">\n    <div class="container" id="notebook-container">    \n{% endblock body_header %}\n\n{% block body_footer %}\n    </div>\n  </div>\n  <footer>\n    <div class="container"\n         style="display:flex; flex-direction: row; justify-content: center; align-items: center;">\n      <p style="margin: 3.7em auto;"> © 2022\n        <a href="https://github.com/sentinel-1" target="_blank">Sentinel-1</a>\n      </p>\n      <!-- TOP.GE ASYNC COUNTER CODE -->\n      <div id="top-ge-counter-container" data-site-id="116052"\n           style="margin-right: 3.7em;float: right;"></div>\n      <script async src="//counter.top.ge/counter.js"></script>\n      <!-- / END OF TOP.GE COUNTER CODE -->\n      <!-- ANALYTICS.LAGOGAL.COM -->\n      <div id="analytics-lagogal-com-access" data-site-id="20221"\n           style="margin: 0;padding: 0;"></div>\n      <script async src="//analytics.lagogal.com/access.js"></script>\n      <!-- / END OF ANALYTICS.LAGOGAL.COM -->\n     </div>\n  </footer>\n</body>\n{% endblock body_footer %}\n')


# 
# *This notebook is originally published under the Apache License (Version 2.0) at the following GitHub repository: [sentinel-1/net_migration_map_Georgia](https://github.com/sentinel-1/net_migration_map_Georgia)*
# 
# For the issues, feedback or suggestions regarding the original notebook (if any) feel free to open an issue at the corresponding [Issues page of the repository](https://github.com/sentinel-1/net_migration_map_Georgia/issues)
