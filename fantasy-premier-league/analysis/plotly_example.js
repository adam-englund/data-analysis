// define columns of interest
const cols_info = [
    'season_year_ending', 'player_name', 'player_position'
];
const cols_response = ['total_points'];
const cols_numeric = [
    'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index', 
    'minutes_x', 'start_cost', 'clean_sheets', 'goals_conceded', 'goals', 'assists_x', 
    'goals_per90', 'assists_per90', 'xg_per90', 'xa_per90', 'npxg_per90', 'npxg_xa_per90',
    'value', 'xg_per90_performance'
];


Plotly.d3.csv(
    'https://raw.githubusercontent.com/adam-englund/data-analysis/main/fantasy-premier-league/data/fpl_fbref_season_player_history.csv', 
    (err, rows) => {
        
        // group data by player and sum total points
        var player_totals = Plotly.d3.nest()
            .key((d) => { return d.player_name;})
            .rollup((d) => { return Plotly.d3.sum(d, (g) => {return g.total_points; }); })
            .entries(rows);
        
        // get the top 10 performers over all seasons
        player_totals.sort((a,b) => { return -a.values - -b.values });
        const top10_players = player_totals.slice(0,10).map((item) => { return item["key"]; });;
        const data_top10 = rows.filter((row) => top10_players.includes(row.player_name));

        // generate the traces for the scatter plot
        traces = []
        top10_players.forEach((player) => {
            filtered_by_player = data_top10.filter((row) => row.player_name === player);
            let trace = { 
                x: filtered_by_player.map((item) => {return item.season_year_ending}), 
                y: filtered_by_player.map((item) => {return item.total_points}), 
                mode: 'lines+markers+text', 
                type: 'scatter', 
                name: player, 
                marker: { size: 12 }
            };
            traces.push(trace);
        });

        // define the plot layout
        var layout = {
            xaxis: { range: [ 2015, 2023 ] },
            yaxis: { range: [50, 350] },
            height: 800,
            legend: { 
                y: 0.5,
                yref: 'paper',
                font: {
                    family: 'Verdana, sans-serif',
                    size: 20,
                    color: 'black',
                }
            },
            title: 'Trends of Highest Performers 2015-2022'
        };

        Plotly.newPlot('plotDiv', traces, layout);

    });
