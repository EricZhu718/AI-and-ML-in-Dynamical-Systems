const express = require('express');
const path = require('path');
const app = express();
const server = require('http').createServer(app);


const port = 3000
const io = require("socket.io")(server)
server.listen(port);

let {PythonShell} = require('python-shell')




app.use(express.json());
app.use(express.static("express"));
// default URL for website
app.use('/', function(req,res){
    res.sendFile(path.join(__dirname+'/express/index.html'));
    //__dirname : It will resolve to your project folder.
  });


console.debug('Server listening on port ' + port);
console.log('Began Running at ' + (new Date()).toString())

io.on('connection', (socket) => {
  console.log("A user has joined")

  socket.on('stock market data request', ({start, end})=> {
    var pyshell = new PythonShell('analysis/import_data.py');
    pyshell.send('1990-01-01')
    pyshell.send('2021-07-12')

    var lastMessage = ""
    pyshell.on('message', function (message) {
      lastMessage = (message)
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err){
            throw err;
        };
        socket.emit('stock market data sent', lastMessage)
        console.log(lastMessage)
        console.log('finished');
    });
    
  })
});


console.log("Done initializing server")