# Lidar3D

# Goal

Vizualize any Wallon place in 3D

# Requirements

* Googlmaps : to extract the latitude, longitude and postcode from the adress entered by the user
* Pyproj : to convert the latitude and longitude into the correct espg format
* Rasterio : to open and work with DSM & DTM files
* Rastertoxyz : to convert .tif into xyz coordinates
* Vtkplotter : to plot the xyz coordinates into 3D render
* Pandas  to read csv files where the xyz coordinates are stored
* Scipy : to help during the plotting

# How it works

* The user is prompted to enter an adress
* When it's the done, the main function start running
* First, the user adress is converted into latitude, longitude and a postcode using the Googlemaps API
* The latitude and longitude are then converted to the coorect ESPG format using Pyproj
* From theses retrieved informations the program can determinate wich county to take the DSM & DTM data from
* Theses files are then opened and cropped into a square around the area of the adress entered by the user
* The cropped square are saved and converted into xyz coordinates
* Theses coordinates are finally used to plot the area in 3D

