let data = {
    party : ['Conservative', 'Labour'],
    ayes : [200,100],
    noes : [50,150],
}

let data2 = [
    {
        party: 'Conservative',
        ayes: 200,
        noes: 50,
        color:"#135789",

    },
    {
        party: 'Labour',
        ayes: 100,
        noes: 150,
        color: "#E0242E"
    }
];


const swidth = 1000 ;
const sheight = 500 ;
const margin = 100;
const width = swidth - 2 * margin;
const height = sheight - 2 * margin;


const maxY = Math.max(...data2.map(d => d.ayes));

console.log(maxY)

const svg = d3.select('svg')
              .attr('width',swidth)
              .attr('height',sheight);

const chart = svg.append('g')
                 .attr('transform', `translate(${margin},${margin})`);

const xScale = d3.scaleLinear()
                 .range([0,width])
                 .domain([0,maxY]);

const yScale = d3.scaleBand()
                .range([height, 0])
                .domain(data2.map(d => d.party));

chart.append('g').call(d3.axisLeft(yScale));



chart.append('g')
     .attr('transform', `translate(0,${height})`)
     .call(d3.axisBottom(xScale))


// add the bars
chart.selectAll()
     .data(data2)
     .enter()
     .append('rect')
     .attr('x', d => 0)
     .attr('y', d => yScale(d.party))
     .attr('height', d => yScale.bandwidth())
     .attr('width', d => xScale(d.ayes))
     .attr ('fill', d => d.color)

// add the grid lines

chart.append('g')
     .attr('class', 'grid')
     .call(d3.axisBottom()
             .scale(xScale)
             .tickSize(height,0,0)
             .tickFormat(''))

svg.append('text')
   .attr('x', width/2)
   .attr('y', margin/2)
   // .attr('text-anchor', 'middle')
   .text('Vote Results')


chart.selectAll('rect')
     .on('mouseenter', function (d, i) {
          d3.select(this).attr('opacity', 0.5)

          chart.append('line')
               .attr('id', 'marker')
               .attr('y1', 0 )
               .attr('x1', xScale(d.ayes))
               .attr('y2', height )
               .attr('x2', xScale(d.ayes))
               .attr('stroke', d.color)
      })
      .on('mouseleave', function (actual, i) {
          d3.select(this).attr('opacity', 1)
          chart.selectAll('#marker')
               .remove()
      })
