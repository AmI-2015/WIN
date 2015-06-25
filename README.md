# WIN (Wc INfo)

How many times did you go to the toilet and once there you found out it was out of service? How long did you wait to enter because of an endless queue and you did not know that a little further on there was a nearly empty toilet?

Our goal is to help you so that this will not happen again!

With WIN every student inside the university will be able to:
- check in real time whether the toilet you are going to is in service or not;
- know the current or average waiting time in queue for the toilet and how many people are there;
- know if there are other toilets nearby where there are no people waiting in queue, so you can choose the best one for you.

A visible indicator, like a light, will inform you about the toilet status and a mobile-friendly interface will inform you about what is going on in the toilets.

Finally, the cleaning staff can let students know when a specific restroom is not available, so that they will be able to work more smoothly.

## MAIN SERVER

The user interface is managed by the files located in "src/server" folder. 

Inside it there are the files for starting the Flask server, connecting with the database, parsing information from sensors.

## DATABASE

Inside "sql" folder there are the files for creating and filling the database.  

## RESTROOM GATEWAY

Each restroom is equipped with a switch selector and a monitor controlled by the files located in "src/gateway" folder.
