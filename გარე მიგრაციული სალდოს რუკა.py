#!/usr/bin/env python
# coding: utf-8

# ## საქართველოს გარე მიგრაციული სალდოს რუკა მოქალაქეობის მიხედვით
# 
# *მინიშნება: მიიტანეთ მაუსი საინფორმაციო მართკუთხედებთან ან სხვადასხვა ქვეყნებთან იმისათვის, რომ გამოჩნდეს შესაბამისი დამატებითი ინფორმაცია.

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


# \* ოთხი საინფორმაციო მართკუთხედი (სენდვიჩის მსგავსი განლაგებით) არის წარმოდგენილი შავ ზღვაში მოცემულ რუკაზე საქართველოს გვერდით, იმისათვის, რომ მათ ასახონ ისეთი მონაცემები რომლების დაკავშირება რომელიმე კონკრეტულ ქვეყანასთან მოცემული რუკის კონტექსტში არ არის შესაძლებელი, როგორიცაა:
# - **Stateless** (მოაქლაქეობის არმქონე პირები) მართკუთხედი: გვიჩვენებს გარე მიგრაციულ სალდოს ისეთი პირებისთვის ვისაც არ გააჩნიათ არცერთი ქვეყნის მოქალაქეობა.
# - **Not stated** (აუღნიშნავი) მართკუთხედი: გვიჩვენებს გარე მიგრაციულ სალდოს ისეთი პირებისთვის რომელთა მოქალაქეობის ინფორმაციაც მონაცემებში არ არის აღნიშნული.
# - **Other** (სხვა) მართკუთხედი: გვიჩვენებს გარე მიგრაციულ სალდოს ისეთი პირებისთვის რომლებიც არიან რომელიმე კონკრეტული ქვეყნის მოქალაქეები, თუმცა მათი ქვეყანა არ არის საქსტატის მიერ გასაჯაროვებული ქვეყნების სიაში და ამიტომ არიან ამ "სხვა" კატეგორიაში თავმოყრილი.
# - **Total** (ჯამი) მართკუთხედი: გვიჩვენებს ჯამურ გარე მიგრაციულ სალდოს მოცემული პერიოდის განმავლობაში და აქ შესულია ყველა მიგრანტის ჯამური სტატისტიკა მათი მოქალაქეობის მიუხედავად.

# # საქართველოს გარე მიგრაციული სალდო
# 
# ზემოთ მოცემული რუკა შექმნილია იმისათვის, რომ გვიჩვენოს საქართველოს გარე მიგრაციული სალდო მოქალაქეობის მიხედვით, შეჯამებული დროის ხანგრძლივ პერიოდზე (მოცემული დროის პერიოდი დამოკიდებულია თავად სტატისტიკური მონაცემების ხელმისაწვდომობაზე). რუკაზე გამოყენებულია ორი ფერის შკალა, წითელი და მწვანე, წითელი შკალა გამოყენებულია ისეთი ქვეყნების აღსანაიშნავად, რომლის მოქალაქეებისთვისაც საქართველოს გარე მიგრაციული სალდო არის ნეგატიური რიცხვი. შესაბამისად, მწვანე შკალა გამოყენებულია ისეთი ქვეყნების აღსანიშნავად, რომლის მოქალაქეებისთვისაც საქართველოს გარე მიგრაციული სალდო დადებითი რიცხვია. თავად ფერის ინტენსივობა კი ორივე ფერის შემთხვევაში მიგვანიშნებს შესაბამისი რიცხვის სიდიდეს (ე.ი. რაც უფრო ინტენსიურია ფერი, მით უფრო დიდია შესაბამისი სტატისტიკური მაჩვენებელი). ქვეყნებისთვის ფერების მინიჭება (წითლად იქნება მონიშნული თუ მწვანედ) და ასევე მათი ფერების ინტენსიურობის შერჩევაც არის ავტომატური პროცესი და დამოკიდებულია მხოლოდ და მხოლოდ შესაბამის სტატისტიკურ მონაცემებზე. აღნიშნული ავტომატური პროცესის ტექნიკური აღწერა და შესაბამისი Python-კოდი სრულიად ღია სახით შეგიძლიათ იხილოთ ამავე დოკუმენტის [ინგლისურენოვან ვერსიაში](../).
# 
# 
# 
# განსაზღვრებები:
#  - **Immigrant** / **იმიგრანტი** (როგორც განსაზღვრულია საქსტატის მიერ) – პირი, რომელმაც გადმოკვეთა საქართველოს საზღვარი და ბოლო 12 თვეში და სულ მცირე 183
#    დღე (შესაძლებელია ეს იყოს რამდენიმე შემოსვლის კუმულაციური ჯამი) იმყოფებოდა საქართველოს
#    ტერიტორიაზე და საქართველო არ იყო მისთვის მუდმივი საცხოვრებელი ქვეყანა, ე.ი. მას საქართველოს
#    საზღვრებს გარეთ წინა 12 თვეში გატარებული აქვს სულ მცირე 183 დღე.
#  - **Emigrant** / **ემიგრანტი** (როგორც განსაზღვრულია საქსტატის მიერ) – პირი, რომელმაც დატოვა საქართველო ბოლო 12 თვეში და სულ მცირე 183 დღე (შესაძლებელია
#    ეს იყოს რამდენიმე გასვლის კუმულაციური ჯამი) იმყოფებოდა სხვა სახელმწიფოს ტერიტორიაზე და
#    საქართველო იყო მისთვის მუდმივი საცხოვრებელი ქვეყანა, ე.ი. მას ქვეყნიდან გასვლამდე წინა 12 თვეში
#    საქართველოში გატარებული ჰქონდა სულ მცირე 183 დღე (ხანგრძლივობის კუმულაციური ჯამი).
#  - **Net migration** / **გარე მიგრაციული სალდო** (როგორც გამოიყენება ამ დოკუმენტში) – მოცემული დროის პერიოდში იმიგრანტთა და ემიგრანტთა რიცხოვნობას შორის სხვაობა.
# 
# 
# 
# გამოყენებული მონაცემები:
# - სტატისტიკური მონაცემები "იმიგრანტების და ემიგრანტების რიცხოვნობა სქესისა და მოქალაქეობის მიხედვით" (Excel ფორმატში) მოპოვებულია 2022 წლის 9 ივნისს საქართველოს სტატისტიკის ეროვნული სამსახურის (საქსტატის) ვებსაიტიდან: [geostat.ge](https://www.geostat.ge/ka/)
# 
# - სტატისტიკური მონაცემები "იმიგრანტების და ემიგრანტების რიცხოვნობა სქესისა და მოქალაქეობის მიხედვით" (CSV ფორმატში) მოპოვებულია 2022 წლის 11 ივნისს საქართველოს სტატისტიკის ეროვნული სამსახურის (საქსტატის) სტატისტიკური მონაცემთა ბაზების ვებსაიტიდან: [pc-axis.geostat.ge](http://pc-axis.geostat.ge/PXWeb/pxweb/ka/Database/)
# - მეტამონაცემები (PDF ფორმატში) მოცემული სტატისტიკური მონაცემებისათვის მოპოვებულია 2022 წლის 14 ივნისს საქართველოს სტატისტიკის ეროვნული სამსახურის (საქსტატის) ვებსაიტიდან: [geostat.ge](https://www.geostat.ge/ka/)
# - რუკის მონაცემები სახელმწიფო საზღვრების შესახებ *(1:10m Cultural Vectors - Admin 0 – Countries - (latest) version 5.1.1)* მოპოვებულია 2022 წლის 11 ივნისს "Natural Earth-ის" ვებსაიტიდან: [naturalearthdata.com](https://www.naturalearthdata.com/)
# 

# In[2]:


get_ipython().run_cell_magic('HTML', '', "<style>\n@media (max-width: 540px) {\n  .output .output_subarea {\n    max-width: 100%;\n  }\n}\n</style>\n<script>\n  $( document ).ready(function(){\n    $('div.input').hide();\n  });\n</script>\n")


# In[3]:


get_ipython().run_cell_magic('capture', '', '%mkdir OGP_classic_ka\n')


# In[4]:


get_ipython().run_cell_magic('capture', '', '%%file "OGP_classic_ka/conf.json"\n{\n  "base_template": "classic",\n  "preprocessors": {\n    "500-metadata": {\n      "type": "nbconvert.preprocessors.ClearMetadataPreprocessor",\n      "enabled": true,\n      "clear_notebook_metadata": true,\n      "clear_cell_metadata": true\n    },\n    "900-files": {\n      "type": "nbconvert.preprocessors.ExtractOutputPreprocessor",\n      "enabled": true\n    }\n  }\n}\n')


# In[5]:


get_ipython().run_cell_magic('capture', '', '%%file "OGP_classic_ka/index.html.j2"\n{%- extends \'classic/index.html.j2\' -%}\n{%- block html_head -%}\n\n{#  OGP attributes for shareability #}\n<meta property="og:url"          content="https://sentinel-1.github.io/net_migration_map_Georgia/ka/" />\n<meta property="og:type"         content="article" />\n<meta property="og:title"        content="საქართველოს გარე მიგრაციული სალდოს რუკა" />\n<meta property="og:description"  content="სტატისტიკური რუკა რომელიც მოქალაქეობის მიხედვით ასახავს საქართველოს გარე მიგრაციულ სალდოს" />\n<meta property="og:image"        content="https://raw.githubusercontent.com/sentinel-1/net_migration_map_Georgia/master/screenshots/2022-06-28_(1200x628).png" />\n<meta property="og:image:alt"    content="Screen Shot of the resulting map" />\n<meta property="og:image:type"   content="image/png" />\n<meta property="og:image:width"  content="1200" />\n<meta property="og:image:height" content="628" />\n    \n<meta property="article:published_time" content="2022-07-05T19:34:45+00:00" />\n<meta property="article:modified_time"  content="{{ resources.iso8610_datetime_utcnow }}" />\n<meta property="article:publisher"      content="https://sentinel-1.github.io" />\n<meta property="article:author"         content="https://github.com/sentinel-1" />\n<meta property="article:section"        content="datascience" />\n<meta property="article:tag"            content="datascience" />\n<meta property="article:tag"            content="geospatialdata" />\n<meta property="article:tag"            content="Python" />\n<meta property="article:tag"            content="data" />\n<meta property="article:tag"            content="analytics" />\n<meta property="article:tag"            content="datavisualization" />\n<meta property="article:tag"            content="bigdataunit" />\n<meta property="article:tag"            content="visualization" />\n<meta property="article:tag"            content="migration" />\n<meta property="article:tag"            content="Georgia" />\n    \n    \n{{ super() }}\n\n{%- endblock html_head -%}\n    \n    \n{% block body_header %}\n<body>\n    \n<div class="container">\n  <nav class="navbar navbar-default">\n    <div class="container-fluid">\n      <ul class="nav nav-pills  navbar-left">\n        <li role="presentation">\n          <a href="/ka/">\n            <svg xmlns="http://www.w3.org/2000/svg"\n                 viewBox="0 0 576 512" width="1em">\n              <path \n                fill="#999999"\nd="M 288,0 574,288 511,288 511,511 352,511 352,352 223,352 223,511 62,511 64,288 0,288 Z"\n              />\n            </svg> Home\n          </a>\n        </li>\n      </ul>\n      <ul class="nav nav-pills  navbar-right">\n        <li role="presentation">\n          <a href="/net_migration_map_Georgia/">🇬🇧 English </a>\n        </li>\n        <li role="presentation" class="active">\n          <a href="/net_migration_map_Georgia/ka/">🇬🇪 ქართული</a>\n        </li>\n      </ul>\n    </div>\n  </nav>\n</div>\n\n\n\n  <div tabindex="-1" id="notebook" class="border-box-sizing">\n    <div class="container" id="notebook-container">    \n{% endblock body_header %}\n\n{% block body_footer %}\n    </div>\n  </div>\n  <footer>\n    <div class="container"\n         style="display:flex; flex-direction: row; justify-content: center; align-items: center;">\n      <p style="margin: 3.7em auto;"> © 2022\n        <a href="https://github.com/sentinel-1" target="_blank">Sentinel-1</a>\n      </p>\n      <!-- TOP.GE ASYNC COUNTER CODE -->\n      <div id="top-ge-counter-container" data-site-id="116052"\n           style="margin-right: 3.7em;float: right;"></div>\n      <script async src="//counter.top.ge/counter.js"></script>\n      <!-- / END OF TOP.GE COUNTER CODE -->\n      <!-- ANALYTICS.LAGOGAL.COM -->\n      <div id="analytics-lagogal-com-access" data-site-id="20221"\n           style="margin: 0;padding: 0;"></div>\n      <script async src="//analytics.lagogal.com/access.js"></script>\n      <!-- / END OF ANALYTICS.LAGOGAL.COM -->\n     </div>\n  </footer>\n</body>\n{% endblock body_footer %}\n')


# *მოცემული დოკუმენტი თავდაპირველად გამოქვეყნებულ იქნა Apache License (Version 2.0) ლიცენზიით შემდეგ GitHub რეპოზიტორზე: [sentinel-1/net_migration_map_Georgia](https://github.com/sentinel-1/net_migration_map_Georgia)*
# 
# მოცემულ დოკუმენტის ორიგინალ ვერსიასთან დაკავშირებულ საკითხებზე შესაბამისი უკუკავშირისათვის, რჩევებისათვის ან შენიშვნებისთვის (თუ რამეა) შეგიძლიათ ახალი Issue-ს შექმნის გზით დააყენოთ საკითხი მისივე GitHub რეპოზიტორის შესაბამის გვერდზე: [Issues page of the repository](https://github.com/sentinel-1/net_migration_map_Georgia/issues)
