# Sensor-Project-Sound
This is a side project I made for a coworker at a previous coop. Through the use of an arduino and some ultrasonic sensors, I was able to automate the testing of the bending of different plastics. The data was gathered through the sensors and then smoothed through the use of an exponential moving average. Every 30 seconds, the new new data was sent to firebase. A google sheet was also created with a script to pull the data from firebase and create important graphs for analysis.
