(function() {
    var ruta = 'http://127.0.0.1:5000';

    fetch(ruta + '/tendencias', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.facultades);
            console.log(data.conteosF);
            console.log(data.estados);
            console.log(data.conteosE);

            // Crear gráfico de distribución por facultad
            Highcharts.chart('container-facultades', {
                chart: {
                    type: 'column'
                },
                title: {
                    align: 'left',
                    text: 'Distribución de Proyectos por Facultad'
                },
                subtitle: {
                    align: 'left',
                    text: 'Fuente: Sistema de Gestión de Proyectos'
                },
                accessibility: {
                    announceNewData: {
                        enabled: true
                    }
                },
                xAxis: {
                    categories: data.facultades,
                    title: {
                        text: 'Facultades'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Número de Proyectos'
                    }
                },
                legend: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            format: '{point.y}'
                        }
                    }
                },
                series: [
                    {
                        name: 'Proyectos',
                        colorByPoint: true,
                        data: data.facultades.map((facultad, index) => ({
                            name: facultad,
                            y: data.conteosF[index]
                        }))
                    }
                ],
                drilldown: {
                    breadcrumbs: {
                        position: {
                            align: 'right'
                        }
                    },
                    series: [] // Puedes añadir series de drilldown aquí si lo deseas
                }
            });

            // Crear gráfico de distribución por estado
            Highcharts.chart('container-estados', {
                chart: {
                    type: 'column'
                },
                title: {
                    align: 'left',
                    text: 'Distribución de Proyectos por Estado'
                },
                subtitle: {
                    align: 'left',
                    text: 'Fuente: Sistema de Gestión de Proyectos'
                },
                accessibility: {
                    announceNewData: {
                        enabled: true
                    }
                },
                xAxis: {
                    categories: data.estados,
                    title: {
                        text: 'Estados'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Número de Proyectos'
                    }
                },
                legend: {
                    enabled: false
                },
                plotOptions: {
                    series: {
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            format: '{point.y}'
                        }
                    }
                },
                series: [
                    {
                        name: 'Proyectos',
                        colorByPoint: true,
                        data: data.estados.map((estado, index) => ({
                            name: estado,
                            y: data.conteosE[index]
                        }))
                    }
                ],
                drilldown: {
                    breadcrumbs: {
                        position: {
                            align: 'right'
                        }
                    },
                    series: [] // Puedes añadir series de drilldown aquí si lo deseas
                }
            });

        } else {
            alert('Error al obtener tendencias: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al obtener las tendencias.');
    });
})();
