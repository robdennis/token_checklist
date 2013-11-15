'use strict';

/* Services */

angular.module('token.services', [])
  .factory('ListService', function($http) {
        return {
            get: function(names) {
                return $http.post('/list', names).then(
                    function(response) {
                        console.log('resolved with: ', response.data);
                        return response.data
                    }
                );
            }
        }
    });
