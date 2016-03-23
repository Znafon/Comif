angular.module('comif.clients-list',
[
  'ui.router',
  'comifServices'
])

.config(function ($stateProvider) {

  $stateProvider
  .state('app.index', {
    url: "/",
    templateUrl: "app/clients-list/clients-list.html",
    controller: 'ClientsListCtrl',
    resolve: {
      clients: function(Client) {
        return Client.query().$promise;
      }
    }
  });

})

.controller('ClientsListCtrl', function ($scope, $state, clients, $rootScope, Message, Modal) {
  $scope.itemsPerPage = 14;
  $scope.clients = clients;

  $scope.detail = function(clientId) {
    $state.go('app.detail', {
      clientId: clientId
    });
  };

  $scope.commande = function(clientId) {
    $state.go('app.commande', {
      clientId: clientId
    });
  }

  $scope.menuOptions = [
    ["Ajouter de l'argent", function($itemScope) {
      Modal.addArgent($itemScope.client);
    }],
    null,
    ["Plus d'informations...", function ($itemScope) {
      $scope.detail($itemScope.client.id);
    }],
  ];

});
