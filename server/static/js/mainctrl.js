app.controller("mainctrl", ["$scope", "$rootScope", "$state", "HttpService",
    function($scope, $rootScope, $state, HttpService) {

        $scope.data = {
            logs: [],
            blists: [],
            rules: [],
        }

        $scope.getAll = function(type) {
            HttpService.get(type, {}, function(response) {
                $scope.data[type + 's'] = response.data;
                console.log($scope.data);
            }, function(err) {
                if (err.data.msg) {
                    alert(err.data.msg);
                } else {
                    alert("很抱歉，发生了未知错误");
                }
            });
        }
    }
]);