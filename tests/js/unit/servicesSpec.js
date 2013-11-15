'use strict';

/* jasmine specs for services go here */

describe('service', function() {
  beforeEach(module('token.services'));


  describe('version', function() {
    it('should return current version', inject(function(ListService, $http) {
      expect(true).toEqual(true);
    }));
  });
});
