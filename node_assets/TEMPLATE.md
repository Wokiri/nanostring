# <p align='center'>**HERE DATA HACKATHON 2020**</p>
## <p align='center'>**Weather Info App**</p>

### Done and Submitted by: [@JWokiri](https://twitter.com/JWokiri). <br/>

### [Youtube overview:](https://youtu.be/0ajBGAlPgsc) <br/>

### [App link:](https://herehackathonapp.herokuapp.com/) <br/>
---
<br/>

**PROJECT OVERVIEW** <br/>
This is a web application that gives weather forecast information for any given place on the globe in accordance to the possibitlies derived from [OPEN WEATHER WEBSITE](https://openweathermap.org/).



<p  align='center'>The scope of this project is aimed at availing the following set of weather information:</p>

- Current weather,
- Minutely forecast for half hour,
- Hourly forecast for 48 hours,
- daily forecast for 3 days and
- Government weather alerts (if and when available).

I have aided your quest for information such as afore mentioned by enabling you to:
1. Interact with HERE TECHNOLOGIES MAP to get weather data of any place by simply tapping the map at that particular place.<br/><br/>
2. Choose a place from an option of atleast 2500 major world cities for which you would desire weather information.<br/><br/>
3. Specify the nature of forecast you wish for the chosen place: i.e;
    - An hour's forecast
    - A day's forecast
    - A week's forecast
4. Get an elaborate weather forecast information that suits your need.

<br/>

**PROJECT IMPLEMENTATION** <br/>
<a href="#first">1. Working on the Frontend</a><br/>
<a href="#second">2. Templating for Backend</a><br/>
<a href="#third">3. Using PostGIS Database</a><br/>
<a href="#fourth">4. Results</a><br/>
<a href="#fifth">5. Statement of Compliance</a><br/><br/>

  ---

## <p id="first">1. Working on the Front End</p>

At the very minimum, a map is displayed and information fetched from Open Weather Data API. Both possibilites leaverage the basic frontend web development tools, i.e. HTML, JAVASCRIPT and CSS.

According to the OpenWeather API documentation, a valid request to its servers must be in a particular format that includes, amongst other variables,
- **lat** => A mandatory floating point numeric  value that represents the latitude of the place,
- **lon** => A mandatory floating point numeric  value that represents the latitude of the place,
- **exclude** => An optional comma separated string values that instructs the time of the forecast needed,
- **API key** => A mandatory alpha numeric string value that enables access to OpenWeather resources.

An example of a valid request would be:
```
https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=hourly,daily&appid={API key}
```

Using the stated frontend development languages, a user is granted access to a map and a forecast-type selection option.

By tapping a point on the map, the coordinates information is obtained from that given clicked point on the map and accordingly appended to the URL. The coordinates may also be obtained by choosing a town or city from a dropdown selection form provided. This data is fished from the postgis database. 'Exclude' values are also appropriately put into the URL as per the user's selection.

[WEBPACK module bundler](https://) has been used to enable easy management of the various dependencies in the course of development of the app. The assets output are minified files that not only, significantly reduce space requirements but are also free from any syntax error in a cases where compilation are successful.

  ---


## <p id="second">2. Templating for Django (Backend)</p>

Being opinionated, Django demands that templates follow a given creteria for templates. It therefore behoves a user to generate Django conforming Templates from the initially Webpack-minified files.

The python file **f_django.py** in this project, located at the base directory of the project reads the webpack-generated HTML file (from templates/prod directory) and uses the read data accordingly to create a django template with the right syntax for appending the necessary static files.

This ensures that all my hashed (from webpack) assets (css, js, png, svg, ....) are properly linked in the html-django format.

f_django.py file sits on the django BASE_DIR from which it able to source the webpack generated html and write a conforming one in the **mapapp** app.

In this project, besides ensuring a successful insertion of static references, it also appends (via include) the form_selection.html and spatialAnalytics.html.
<br/><br/>

  ---

  ## <p id="third">3. Using PostGIS Database</p>

POSTGIS database has been used in this application primarily to harness the applicable spatial (topological) analysis options.

Also, it will be seen that the major cities are fetched from the database. It was needful to store this data in the database because they are geometric points with spatitial attributes which are read to identify their respective lat and lon values.

**HOWEVER,** following my choice to create the app with Joharnessburg data, this spatial possibility is available only for South Africa, Jg.

  ---

  ## <p id="fourth">4. Results</p>

<p>When a place has been identified and weather forecast parameters well specified, the weather app gives results in various formats and segments.</p>


1. Tap a place on the map, or choose a city from the selection;

You will see a circular shape of 2KM radius whose center is the coordinates used to fetch the weather data. This is done on the assumption that the given weather results applies to places within that radius.

2. Upon hovering on the circular shape, a pane containing a summary of the reults is shown just above the map.

This gives you a weather summary of what I would consider fundamental weather elements for a quick overview. You have an option of clicking a link to a detailed information segment or choose a different place for that other places' information.

- The button ***Clear Map Objects*** removes the circular shape and summary pane.
- The button ***World View*** zooms the planet to a full world view.
- Long pressing the circle object clears the map.
- Clicking the summary pane removes it from the DOM.

3. The link to the detailed information takes you to the detailed section where you will access all results fetched from Open weather.

This has a much broader weather results many of which were not given in the summary.

It is here also that, if you are in South Africa results for spatial analysis will be displayed also.

Spatial Analysis:
The circle seen in the map is somehow replicated by a geojson information generated by this [code](https://github.com/Wokiri/GIS-in-CODE/blob/master/src/circleGeojson.js). It is this geojson whose values are POSTED into the data base with which the spatial querry is performed. 

  ---

   ## <p id="fifth">5. Statement Compliance to Hackathon Guidelines</p>

   I here acknowledge reading and understanding the [HERE HACHATHON RULES OF PARTICIPATION](https://herehackathon.devpost.com). I am pleased to affirm my absolute, unconditional compliance; and to the best of my knowledge:
   - I have observed the dates and timings,
   - I am an eligible participant (on an individual basis),
   - I have included a link to my solution code on GitHub,
   - I have created a video that includes footage clearly explaining my solution’s features and functionality,
   - I have made my submissions in English language.

   These and any other applicable rules I have observed.

   ---

## Reach Out...

<p align='center'><a href="https://twitter.com/JWokiri"><img height="30" src="https://www.flaticon.com/svg/static/icons/svg/145/145812.svg"></a>&nbsp;&nbsp;&nbsp
<a href="mailto:wokirijoe@gmail.com"><img height="30" src="https://www.flaticon.com/svg/static/icons/svg/732/732200.svg"></a>&nbsp;&nbsp;&nbsp;
<a href="https://github.com/Wokiri"><img height="30" src="https://www.flaticon.com/svg/static/icons/svg/2111/2111425.svg"></a></p>
