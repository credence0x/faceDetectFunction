# Face Detector Function
Hey there :wave: :grinning:. <br><br>
This is the second of two parts of a loosely coupled application.

It is a face detection application and consists of;<br>
      <br>a) an interface that the user communicates with (<a href="https://github.com/ojetokun/face-detect-interface"> which can be found here </a>)
      <br>b) a machine learning function that interpretes the images sent by the interface. ( this part )
<br><br>
 
This is the function that has all the logic for the face detection aspect. It receives api calls then uses the weights of the pre-trained model to detect faces sent to it by the interface side.<br>
After processing the image, it sends it out. 
<br>It however firstly authenticates that the request is coming from the face detect interface (the first part )else it rejects the request.<br>
Also, after making sure that it came from the first app, it further authenticates the user's credentials by sending out an api call to the first app.
<br>
<br>
The function is written in python django and the other side is written in javascript node.js. 
<br>The reason for writing the machine learning functions in python is that python has more support and is easier to use for data science.
<br> I have also been using python for data science for a long while so that seemed to be a better option.
<br><br>
Note: The project has been completed but has been removed from production due to cost of management  but a picture of it working can be found at https://twitter.com/ojetokunlanre/status/1424799067461210141/photo/1
<br><br>

