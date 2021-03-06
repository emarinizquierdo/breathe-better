'use strict';

angular.module('datafestApp')
    .controller('MainCtrl', function($rootScope, $scope, $http, $mdBottomSheet, $interval, MainMap, chart, shData, Aire, pollution, weather, geoloc, toxic, route, geometry) {

        var weatherLayer;
        var cloudLayer;

        $rootScope.directions = {
            origin: null,
            destination: null
        };

        $scope.weatherButtonActive = false;
        $scope.pollutionButtonActive = true;

        /* Shared Data */
        $scope.shData = shData;

        $scope.shData.day = new Date();
        $scope.shData.day.setHours($scope.shData.day.getHours() - 3);
        $scope.shData.day.setMinutes(0);
        $scope.shData.day.setSeconds(0);
        $scope.shData.day.setMilliseconds(0);

        shData.pollutionParameter = 14;

        $scope.toxic = toxic;
        $scope.travelMode = MainMap.travelMode;
        $scope.toxicElement = 1;

        $scope.distanceInfo = route.distanceInfo;

        $scope.shData.updateDay = function() {
            $scope.pollutionButtonActive = true;
            pollution.get($scope.shData.day, $scope.shData.pollutionParameter, function(data) {

                pollution.paintHeatmap(data);
                pollution.paintStations(data);
            });
        }

        function computeTotalDistance(result) {

            var total = 0;
            var points = [];

            var myroute = result.getDirections().routes[0];
            for (var i = 0; i < myroute.legs.length; i++) {
                total += myroute.legs[i].distance.value;
            }

            total = total / 1000;
            $scope.distance = total;


            $rootScope.directions.origin = result.directions.routes[0].legs[0].start_address;
            points.push({
                lat: result.directions.routes[0].legs[0].start_location.lat(),
                long: result.directions.routes[0].legs[0].start_location.lng()
            });

            if (result.directions.routes[0].legs[0].via_waypoints && (result.directions.routes[0].legs[0].via_waypoints.length > 0)) {
                for (var i = 0; i < result.directions.routes[0].legs[0].via_waypoints.length; i++) {
                    points.push({
                        lat: result.directions.routes[0].legs[0].via_waypoints[i].lat(),
                        long: result.directions.routes[0].legs[0].via_waypoints[i].lng()
                    });
                }
            }

            $rootScope.directions.destination = result.directions.routes[0].legs[0].end_address;
            points.push({
                lat: result.directions.routes[0].legs[0].end_location.lat(),
                long: result.directions.routes[0].legs[0].end_location.lng()
            });

            route.getRoute(points, geometry.avoidBoundingBoxes).then(function(p_route) {
                route.paintLine(p_route);
            });

            secureApply();

        }

        var secureApply = function() {
            if (!$rootScope.$$phase) {
                $rootScope.$apply();
            }
        }

        $scope.togglePollution = function() {

            if ($scope.pollutionButtonActive) {

                pollution.get($scope.shData.day, $scope.shData.pollutionParameter, _paintPollution);


            } else if (MainMap.objects.heatmap) {

                geometry.deleteRectangles();
                MainMap.objects.heatmap.setMap(null);

            }
        }

        $scope.showGridBottomSheet = function($event) {
            $mdBottomSheet.show({
                templateUrl: 'app/sheet/sheet.html',
                controller: 'SheetCtrl',
                targetEvent: $event
            }).then(function(clickedItem) {

            });
        };

        $scope.changeTravelMode = function() {
            MainMap.travelMode = $scope.travelMode;
            MainMap.calcRoute($rootScope.directions.origin, $rootScope.directions.destination);
        };



        var _paintPollution = function(data) {

            pollution.paintHeatmap(data);

            geometry.paintRectangle(data);

            MainMap.calcRoute($rootScope.directions.origin, $rootScope.directions.destination);

        }

        var _rotateToxicElement = function() {
            $scope.toxicElement = ($scope.toxicElement > 4) ? 1 : $scope.toxicElement + 1;
        };


        $interval(_rotateToxicElement, 6000);


        MainMap.initialize(function() {

            pollution.get($scope.shData.day, $scope.shData.pollutionParameter, pollution.paintHeatmap);
            pollution.paintStations();

            chart.elevator = new google.maps.ElevationService();
            chart.chart = new google.visualization.AreaChart(document.getElementById('elevation_chart'));

        });

        MainMap.addEventHandler(MainMap.objects.directionsDisplay, function(data) {
            computeTotalDistance(MainMap.objects.directionsDisplay);
            var route = MainMap.objects.directionsDisplay.getDirections().routes[0];
            chart.drawPath(route.overview_path);
        })


        /* Interfaces */
        $scope.toggleWeather = weather.toggleWeather;
        $scope.GoToRealPos = geoloc.GoToRealPos;
        $scope.calcRoute = MainMap.calcRoute;
    });
