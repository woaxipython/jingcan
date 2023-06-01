function lineCharts(name = "", stack = "", type = "line", areaStyle = null) {
    return {
        name: name,
        type: type,
        stack: stack,
        smooth: true,
        label: {
            show: false,
            position: 'top'
        },
        emphasis: {
            focus: 'series'
        },
        data: [],
        areaStyle: areaStyle
    };
}

function XOpention(xAxisData, seriesData, title) {
    return {
        toolbox: {
            show: true,
            // orient: 'vertical',
            left: 'left',
            top: 'top',
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            },
            itemSize: 14
        },
        title: {
            text: title,
            right: "center",
            bottom: "92%"
        },
        grid: {
            containLabel: true,
            left: "left",
            right: "10%",
            height: "60%",
        },
        dataZoom: [
            {
                orient: 'vertical',
                id: 'dataZoomX',
                type: 'slider',
                xAxisIndex: [0],
                filterMode: 'filter',
                height: "70%",
                bottom: "center",
                right: "2%",
                width: 12,
            },],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            },
        },
        legend: {
            type: "scroll",
            right: "center",
            bottom: '1%',
            orient: 'horizontal',
            // orient: 'vertical',
        },
        xAxis: {data: xAxisData,},
        yAxis: {},
        series: seriesData,
        bottom: "0"
    };
}


function zGMapOption(jsonUrl = "../static/json/ZG.json", mapChart = null, data = null, name = "销售额", max = 35000, min = 0) {
    $.get(jsonUrl, function (geoJson) {
        echarts.registerMap('ZG', geoJson);
        option = {
            backgroundColor: 'transparent',
            title: {
                text: "",
                x: 'center',
                textStyle: {
                    color: '#2c2c2c'
                }
            },
            toolbox: {
                show: true,
                //orient: 'vertical',
                left: 'left',
                top: 'top',
                feature: {
                    dataView: {readOnly: false},
                    restore: {},
                    saveAsImage: {}
                }
            },
            tooltip: {
                trigger: 'item'
            },
            colorBy: "series",
            color: ['#5470c6', '#91cc75', '#ee6666', '#73c0de', '#3ba272', "#fc8452", "#9a60b4", "#ea7ccc"],
            gradientColor: ['#f6efa6', '#d88273', '#bf444c'],
            visualMap: {
                left: 'right',
                min: min,
                max: max,
                inRange: {
                    color: [
                        '#313695',
                        '#4575b4',
                        '#74add1',
                        '#abd9e9',
                        '#e0f3f8',
                        '#ffffbf',
                        '#fee090',
                        '#fdae61',
                        '#f46d43',
                        '#d73027',
                        '#a50026'
                    ]
                },
                text: ['High', 'Low'],
                calculable: true
            },
            series: [
                {
                    name: '销售额',
                    type: 'map',
                    map: 'ZG',
                    roam: true,

                    mapLocation: {
                        y: 60
                    },
                    itemSytle: {
                        emphasis: {label: {show: true}}
                    },
                    data: data
                }
            ],

        };
        mapChart.setOption(option);
    });
}

function YOpention(yAxisData, seriesData) {
    return {
        backgroundColor: '#fff',
        toolbox: {
            orient: 'vertical',
            show: false,
            top: "10%",
            feature: {
                dataZoom: {
                    yAxisIndex: "none"
                },
                dataView: {
                    readOnly: false
                },
                magicType: {
                    type: ["line", "bar"]
                },
                restore: {},
                saveAsImage: {}
            },
            itemSize: 14
        },
        grid: {
            show: false,
            containLabel: false,
            left: "0%",
            right: "0%",
        },
        dataZoom: [
            {
                show: false,
                id: 'dataZoomX',
                type: 'slider',
                xAxisIndex: [0],
                filterMode: 'filter',
                height: 15,
                bottom: "11%",
            },],
        tooltip: {
            confine: false,
            trigger: 'axis',
            z: 999,
            axisPointer: {
                type: 'cross',

                label: {
                    backgroundColor: '#6a7985',
                }
            },
        },
        legend: {
            show: false,
            type: "scroll",
            right: "center",
            bottom: '1%'
        },
        xAxis: {
            show: false
        },
        yAxis: {
            show: false,
            data: yAxisData,
        },
        series: seriesData,
        bottom: "0"
    };
}

function weekTimeOption(hours, days, data) {
    return option = {
        tooltip: {
            position: 'top'
        },
        toolbox: {
            show: true,
            //orient: 'vertical',
            left: 'left',
            top: 'top',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        grid: {
            height: '75%',
            top: '15%'
        },
        xAxis: {
            type: 'category',
            data: hours,
            splitArea: {
                show: true
            }
        },
        yAxis: {
            type: 'category',
            data: days,
            splitArea: {
                show: true
            }
        },
        visualMap: {
            min: 300,
            max: 6000,
            calculable: true,
            orient: 'vertical',
            left: 'right',
            right: '3%',
        },
        series: [
            {
                name: '销售额',
                type: 'heatmap',
                data: data,
                label: {
                    show: false
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

}