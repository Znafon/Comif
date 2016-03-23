angular.module('comifHelpers', ['ui.bootstrap'])

.controller('MessagesCtrl', function ($scope, $timeout) {
  $scope.messages = [];

  $scope.$on('message', function (event, message) {
    $scope.messages.push(message);

    $timeout(function() {
      $scope.messages.shift();
    }, 4000);
  })
})

.controller('ModalCtrl', function ($scope, $uibModal, $rootScope) {

  $scope.$on('modal-add-argent', function(event, client) {
    $scope.client = client;

    $uibModal.open({
      animation: true,
      templateUrl: 'Helpers/modals/addArgent.html',
      scope: $scope,
      controller: 'ModalAddArgentCtrl'
    })
  });

})

.controller('ModalAddArgentCtrl', function($scope, $uibModalInstance, Client, Message, $rootScope) {
  $scope.moyen = "Carte bancaire";

  $scope.ok = function () {
    c = $scope.client;
    c.solde = parseFloat($scope.montant) + parseFloat(c.solde);
    Client.update({clientId: $scope.client.id}, {amount: parseFloat($scope.montant)}, function (data) {
      Message.info("Le solde de "+$scope.client.nom + " est maintenant de "+ c.solde+ " €");
    }, function (data) {
      Message.danger("Oops, le solde de "+ $scope.client.nom +" n'a pas pu être mis à jour", data.statusText);
    });
    $uibModalInstance.close('cancel');
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
})


.directive('autofocus', ['$timeout', function($timeout) {
  return {
    restrict: 'A',
    link : function($scope, $element) {
      $timeout(function() {
        $element[0].focus();
      });
    }
  }
}])

.controller('ControlSidebarCtrl', function ($scope, $rootScope) {

  $scope.click = function () {

    $rootScope.$broadcast('toggle-sidebar');
  };
});
