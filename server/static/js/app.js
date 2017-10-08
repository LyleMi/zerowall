"use strict";

var app = angular.module("pocer", ["ui.router"]);

app.run(["$rootScope", function($rootScope) {}]);

app.config(["$stateProvider", "$urlRouterProvider", function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/");

    $stateProvider
        .state("notfound", {
            url: "/notfound",
            templateUrl: "static/templates/404.html",
        });

}]);