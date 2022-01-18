
const socket = io.connect('http://localhost:3000')




function makeNewGraph(data) {
    const totalWidth = 900
    const totalHeight = 500

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 40, bottom: 30, left: 100},
        width = totalWidth - margin.left - margin.right,
        height = totalHeight - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var sVg = d3.select("#chart_svg")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    // translate this svg element to leave some margin.
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // X scale and Axis
    var x = d3.scaleLinear()
    .domain([0, d3.max(data, function(d) { return +d.x; })])         // This is the min and the max of the data: 0 to 100 if percentages
    .range([0, width]);       // This is the corresponding value I want in Pixel
    sVg
    .append('g')
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

    // Y scale and Axis
    var y = d3.scaleLinear()
    .domain([0, d3.max(data, function(d) { return +d.y; })])         // This is the min and the max of the data: 0 to 100 if percentages
    .range([height, 0]);       // This is the corresponding value I want in Pixel
    sVg
    .append('g')
    .call(d3.axisLeft(y));

    // Add the line
    sVg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d.x) })
        .y(function(d) { return y(d.y) })
      )
}





$.post('http://localhost:3000/loadData', {start: '1990-01-01', end: '2021-07-12'}, function(data, status) {
    // console.log('recieved')
    // console.log(JSON.parse(data))
    data = JSON.parse(data)


    // earliest date
    var startDate = new Date(parseInt(Object.keys(data.Open)))
    var startDateEpoch = parseInt(Object.keys(data.Open))
    
    // get point pairs from JSON
    var reshapedArr = []
    for (var key in data.Open) {
        reshapedArr.push({x: (key - startDateEpoch)/86400000, y:data.Open[key]})
    }

    console.log(reshapedArr)
    console.log(startDate)

    makeNewGraph(reshapedArr)


    var sVg = d3.select("#chart_svg")
    
    // console.log(reshapedArr.length)
})



// socket.emit('stock market data request', {start: '1990-01-01', end: '2021-07-12'})


// socket.on('stock market data sent', function (message) {
    // recieves stock market data
//     console.log(JSON.parse(message))
// });