function getAllData() { //Defining my function
  var firebaseUrl = "https://work-5b7b6.firebaseio.com/"; //Storing the url of my firebase database
  var base = FirebaseApp.getDatabaseByUrl(firebaseUrl); //Setting this url to the database I'll be pulling information from
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); //Getting the spreadsheet that I will make changes to
  var name = sheet.getRange(1,2); //Saving the place where the test name the user entered 
  var data = name.getValue(); //Saving the test name itself
  var test = base.getData(data); //Pulling from that specific test in my database
  
  sheet.clear(); //Clears the entire sheet
  
  sheet.appendRow(["Enter Test Name Beside:", ""]); //Writing area I want to be present for when the user wants to show a certain test
  sheet.appendRow(["Time", "Distance 1", "Distance 2", "Angle 1", "Angle 2", "Center Dist", "Length"]); //Giving headers to each of the columns
  
  for(var i in test) { //Code will run over and over again for each data entry in the database
    
    sheetRowDist = []; //Defining an array, will be used to store information I want to add (Note at the start of every iteration it will be empty)
    dist1 = test[i].dist; //Stores the distance 1 value in this specific data entry
    dist2 = test[i].dist2; //Stores the distance 2 value in this specific data entry
    
    distEnd = 21 //the distance the sensors are from end of sash
    
    angle1 = (Math.asin((test[i].dist)/distEnd))*(180/(Math.PI)); //Calculates the angle on the first sensor's side
    angle2 = (Math.asin((test[i].dist2)/distEnd))*(180/(Math.PI)); //Calculates the angle on the second sensor's side
    distMid = (5/16)*((angle1+angle2)/2); //Ccalculating the middue distance of the sash
    
    sashLength = 84 //Length of sash
    hsl = sashLength/2 //Calculatng half sash length
      
    if (distMid == 0) { //Code will run if the sash has not deflected
      length = sashLength; //Setting length to the original
    }
    else{ //Code will only run if sash has deflected 
      length = Math.sqrt(hsl*hsl+4*(distMid*distMid)) + ((hsl*hsl)/(2*distMid))*(Math.log((2*distMid/hsl) + Math.sqrt((2*distMid/hsl)*(2*distMid/hsl)+1))); //Function to calculate new length of sash
    }
    
    sheetRowDist.push(test[i].time, dist1, dist2, angle1, angle2, distMid, length); //Adding all the gathered information into an array
    sheet.appendRow(sheetRowDist); //Adding every item in the array to a cell in a new row
  }
  
  createChart(sheet); //Calling on the function below to run that code
}

function createChart(sheet) { //Defining function
  
  var range = sheet.getRange("A2:C100"); //Saving the information I want to use in my chart
  var chart = sheet.getCharts()[0]; //Defining which chart I want to update
  chart = chart.modify() //Modifying function by doing whatever is below 
     .addRange(range) //Setting the data in my sheet, which is now updated from firebase, to the data of the chart 
     .setOption('title', 'Sash Deflection Distances') //Setting the title
     .setOption('animation.duration', 500) //Animating the creation of the graph
     .setPosition(9,9,0,0) //Setting the graph's position in the spreadsheet
     .build(); //Building the chart
  sheet.updateChart(chart); //Updating the old chart to the new chart
}

