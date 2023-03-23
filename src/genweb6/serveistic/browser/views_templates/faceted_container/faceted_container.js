$.urlParam = function(name){

  var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
  return results ? results[1] : false;

}

$.showFilters = function(){

  if($.urlParam('c4') || $.urlParam('c5') || $.urlParam('c6') || $.urlParam('c7') || $.urlParam('c8') || $.urlParam('c9') || $.urlParam('c10') || $.urlParam('c11')){

    setTimeout(function(){

      const bsCollapse = new bootstrap.Collapse('#collapseFilters', {
        show: true
      });

    }, 1000);

  }

}

$.checkFiltersTogglePopular = function(){

  setInterval(function(){

    if($.urlParam('c0') || $.urlParam('c4') || $.urlParam('c5') || $.urlParam('c6') || $.urlParam('c7') || $.urlParam('c8') || $.urlParam('c9') || $.urlParam('c10') || $.urlParam('c11')){

      $('#popular').hide();

    } else {

      $('#popular').show();

    }

  }, 250);

}

$(document).ready(function(){

  $.showFilters();

  $.checkFiltersTogglePopular();

});
