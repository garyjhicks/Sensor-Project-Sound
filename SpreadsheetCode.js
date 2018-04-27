function getAllData() { 
  var firebaseUrl = "https://work-5b7b6.firebaseio.com/"; 
  var base = FirebaseApp.getDatabaseByUrl(firebaseUrl); 
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); 
  var name = sheet.getRange(1,2);  
  var data = name.getValue(); 
  var test = base.getData(data); 
  
  sheet.clear(); 
  
  sheet.appendRow(["Enter Test Name Beside:", ""]); 
  sheet.appendRow(["Time", "Distance 1", "Distance 2", "Angle 1", "Angle 2", "Center Dist", "Length"]); 
  
  for(var i in test) { 
    
    sheetRowDist = []; 
    dist1 = test[i].dist; 
    dist2 = test[i].dist2; 
    
    distEnd = 21
    
    angle1 = (Math.asin((test[i].dist)/distEnd))*(180/(Math.PI)); 
    angle2 = (Math.asin((test[i].dist2)/distEnd))*(180/(Math.PI)); 
    distMid = (5/16)*((angle1+angle2)/2); 
    
    sashLength = 84 
    hsl = sashLength/2 
      
    if (distMid == 0) { 
      length = sashLength; 
    }
    else{ 
      length = Math.sqrt(hsl*hsl+4*(distMid*distMid)) + ((hsl*hsl)/(2*distMid))*(Math.log((2*distMid/hsl) + Math.sqrt((2*distMid/hsl)*(2*distMid/hsl)+1))); //Function to calculate new length of sash
    }
    
    sheetRowDist.push(test[i].time, dist1, dist2, angle1, angle2, distMid, length); 
    sheet.appendRow(sheetRowDist); 
  }
  
  createChart(sheet); 
}

function createChart(sheet) { 
  
  var range = sheet.getRange("A2:C100"); 
  var chart = sheet.getCharts()[0]; 
  chart = chart.modify()  
     .addRange(range) 
     .setOption('title', 'Sash Deflection Distances') 
     .setOption('animation.duration', 500) 
     .setPosition(9,9,0,0) 
     .build(); 
  sheet.updateChart(chart); 
}

