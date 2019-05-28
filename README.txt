

by Yiming Fang(yf2484@columbia.edu), Yutian Lin(yl4094@columbia.edu), Zeyi Liu(zl2753@columbia.edu), Yuanbo Li(yl4092@columbia.edu)

Part A.General Introduction 

1.The program is written for Columbia students who want to find restaurants near them. Students will be able to find restaurants that best suit their needs, and the result will be displayed on the map.

2.This program uses Google Map API

3.Files:
Main.html (main method)
Directory Pic 
Directory Database (stores database (.json file) and web-crawler for data update)


Part B.Data Collection
We use Yelp Fusion API to grab data of 20 restaurants near Columbia University for dinner.
We rearrange and write the data to a .json file, which we later use to obtain 5 most-matched restaurants.

Part C.Algorithm 

The algorithm is based on the following considerations:

1.If a user indicates more than two kinds of foods as his/hers preference(ex. "desserts" & "burger"), then these factors would be considered with relevant weights, and restaurants	 satisfying both components will be selected.

2.Since data is collected from Yelp API (see part B), the ratings on Yelp.com will be partially considered to evaluate the quality and popularity of a restaurant

3.If user enabled "available now" mode, the program will automatically rule out all restaurants that are not open at time of their search

4.Even if "burger" or "desserts" does not appear on user's choice, popular restaurants like Community might still appear after calculation. (It's always not bad to eat at Community lol)

5.After a set of restaurants have been selected to fit the user's preferences, their location will be shown on the map provided by Google API, and short description of them can be found on this page as well

6.John Jay Dining Hall will ALWAYS appear as the first choice :)

