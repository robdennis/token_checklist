'use strict';

/* Controllers */

angular.module('token.controllers', ['token.services']).
    controller('TokenEntryControl', ['$scope', 'ListService', function($scope, ListService) {
        $scope.message = 'Welcome to Token Entry';
        $scope.list = [
            "Trostani's Summoner", 'Saber Ants',
            'Hornet Queen', 'Unknown Name'
        ].join('\n');

        $scope.getTokensFromList = function() {
            ListService.get($scope.list).then(function(data) {
                $scope.results = data;
            });
        }
    }]);