angular.module('comif.sidebar',
[
  'comifHelpers'
])

.controller('SidebarCtrl', function($scope, Modal) {
  $scope.status = false;

  $scope.$on('toggle-sidebar', function () {
    $scope.status = !$scope.status;
  });
  
  $scope.addClient = function() {
    Modal.addClient();
  }
});
