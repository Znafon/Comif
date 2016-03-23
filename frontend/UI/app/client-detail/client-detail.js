angular.module('comif.client-detail',
[
  'ui.router',
  'comifServices'
])

.config(function ($stateProvider) {

  $stateProvider
  .state('app.detail', {
    url: '/client/:clientId',
    templateUrl: 'app/client-detail/client-detail.html',
    controller: 'ClientDetailCtrl'
  });

})

.controller('ClientDetailCtrl', function ($scope, $rootScope, $stateParams, Client, Message) {
  $scope.client = Client.get({clientId: $stateParams.clientId});

  $scope.modifier = {
    nom: false,
    solde: false
  };
  $scope.nouveau = $scope.client;


  $scope.updateNom = function (nom) {
    c = $scope.client;
    c.nom = nom;
    Client.update({clientId: c.id}, c, function (data) {
      Message.info($scope.client.nom + " a été mis à jour");
      $scope.client.nom = nom;
    }, function (data) {
      Message.danger("Oops, "+ $scope.client.nom +" n'a pas pu être mis à jour", data.statusText);
    });
    $scope.modifier.nom = false;
  }

  $scope.updateSolde = function(solde) {
    c = $scope.client;
    c.solde = solde;
    Client.update({clientId: c.id}, c, function (data) {
      Message.info("Le nouveau solde de "+ $scope.client.nom + " est "+ solde +" €");
      $scope.client.solde = solde;
    }, function (data) {
      Message.danger("Oops, le solde de "+ $scope.client.nom +" n'a pas pu être mis à jour", data.statusText);
    });
    $scope.modifier.solde = false;
  }

  $scope.escape = function($event) {
    if($event !== undefined) {
      $event.preventDefault();
    }
    $scope.modifier.nom = false;
    $scope.modifier.solde = false;
  }
});
