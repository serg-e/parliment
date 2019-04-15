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

    },
    {
        party: 'Labour',
        ayes: 100,
        noes: 150,
    }
];


const margin = 100;
const width = 1000 - 2 * margin;
const height = 600 - 2 * margin;


const maxY = Math.max(...data2.map(d => d.ayes));

console.log(maxY)

const svg = d3.select('svg')
              .attr('width',1000)
              .attr('height',600);

const chart = svg.append('g')
                 .attr('transform', `translate(${margin},${margin})`);

const yScale = d3.scaleLinear()
                 .range([height,0])
                 .domain([0,maxY]);

chart.append('g').call(d3.axisLeft(yScale));

const xScale = d3.scaleBand()
                 .range([0,width])
                 .domain(data2.map(d => d.party));

chart.append('g')
     .attr('transform', `translate(0,${height})`)
     .call(d3.axisBottom(xScale))


// add the bars
chart.selectAll()
     .data(data2)
     .enter()
     .append('rect')
     .attr('x', d => xScale(d.party))
     .attr('y', d => yScale(d.ayes))
     .attr('width', d => xScale.bandwidth()-50)
     .attr('height', d => height - yScale(d.ayes))

// add the grid lines

chart.append('g')
     .attr('class', 'grid')
     .call(d3.axisLeft()
             .scale(yScale)
             .tickSize(-width,0,0)
             .tickFormat(''))

svg.append('text')
   .attr('x', width/2)
   .attr('y', margin/2)
   // .attr('text-anchor', 'middle')
   .text('Vote Results')


chart.selectAll('rect')
      .on('mouseenter', function (actual, i) {
          d3.select(this).attr('opacity', 0.5)
      })
      .on('mouseleave', function (actual, i) {
          d3.select(this).attr('opacity', 1)
      })
