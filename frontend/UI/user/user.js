angular.module('comif.user',
[
  'comifServices'
])


.controller('UserCtrl', function(User, $scope, $state) {
  $scope.username = User.username();

  $scope.logout = function () {
    User.logout();
  };

  $scope.$on('logout', function () {
    $state.go('login');
  });
});
