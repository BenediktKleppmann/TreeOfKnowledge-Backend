(function () {
  'use strict';

  angular.module('TreeOfKnowledgeApp', [])

  .controller('TreeOfKnowledgeController', ['$scope', '$log',
    function($scope, $log) {
      $scope.getResults = function() {
        $log.log("test");
      };
    }
  ]);

}());