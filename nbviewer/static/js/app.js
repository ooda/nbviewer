/* Author: Hugues Demers
 * Copyrights 2013
  
*/
/*global appConfig:false */
define([
  "jquery",
  "underscore",
  "knockout",
  "viewmodel",
],
function ($, _, ko, viewmodel) {
  var exports = {};

  exports.initialize = function () {
    console.log("Initializing app.");
    ko.applyBindings(viewmodel);
  };

  return exports;
});
