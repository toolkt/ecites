odoo.define('ecites.utils', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');

var qweb = core.qweb;

console.log("Utils Loaded");
/**
 * Allows the given input to propose existing website URLs.
 *
 * @param {ServicesMixin|Widget} self - an element capable to trigger an RPC
 * @param {jQuery} $input
 */
function autocompleteCountry(self, $input) {
    $input.autocomplete({
        source: function (request, response) {
            return self._rpc({
                    model: 'res.country',
                    method: 'search_record',
                    args: [null, request.term],
                    kwargs: {
                        limit: 15,
                    },
                }).then(function (exists) {
                    console.log(exists);
                    var rs = _.map(exists, function (r) {
                        return r;
                    });
                    response(rs.sort());
                });
            
        },
        select: function (ev, ui) {
            $input.val(ui.item.label);
            // $input.next().val(ui.item.value);
            return false;
        },
        change: function( ev, ui ) {
            // console.log(ev,ui);
            if (!ui.item){
                $input.val('');
                $input.next().val('');
            }
        },
        autoFocus: true,
    });
}
/**
 * Allows the given input to propose existing website URLs.
 *
 * @param {ServicesMixin|Widget} self - an element capable to trigger an RPC
 * @param {jQuery} $input
 */
function autocompleteProvince(self, $input) {
    $input.autocomplete({
        source: function (request, response) {
            return self._rpc({
                    model: 'res.province',
                    method: 'search_record',
                    args: [null, request.term],
                    kwargs: {
                        limit: 15,
                    },
                }).then(function (exists) {
                    console.log(exists);
                    var rs = _.map(exists, function (r) {
                        return r;
                    });
                    response(rs.sort());
                });
            
        },
        select: function (ev, ui) {
            $input.val(ui.item.label);
            // $input.next().val(ui.item.value);
            return false;
        },
        change: function( ev, ui ) {
            // console.log(ev,ui);
            if (!ui.item){
                $input.val('');
                $input.next().val('');
            }
        },
        autoFocus: true,
    });
}


/**
 * Allows the given input to propose existing website URLs.
 *
 * @param {ServicesMixin|Widget} self - an element capable to trigger an RPC
 * @param {jQuery} $input
 */
function autocompleteBrgy(self, $input) {
    $input.autocomplete({
        source: function (request, response) {
            return self._rpc({
                    model: 'res.brgy',
                    method: 'search_record',
                    args: [null, request.term],
                    kwargs: {
                        limit: 15,
                    },
                }).then(function (exists) {
                    console.log(exists);
                    var rs = _.map(exists, function (r) {
                        return r;
                    });
                    response(rs.sort());
                });
            
        },
        select: function (ev, ui) {
            $input.val(ui.item.label);
            // $input.next().val(ui.item.value);
            return false;
        },
        change: function( ev, ui ) {
            // console.log(ev,ui);
            if (!ui.item){
                $input.val('');
                $input.next().val('');
            }
        },
        autoFocus: true,
    });
}

/**
 * Allows the given input to propose existing website URLs.
 *
 * @param {ServicesMixin|Widget} self - an element capable to trigger an RPC
 * @param {jQuery} $input
 */
function autocompleteCityMun(self, $input) {
    $input.autocomplete({
        source: function (request, response) {
            return self._rpc({
                    model: 'res.citymun',
                    method: 'search_record',
                    args: [null, request.term],
                    kwargs: {
                        limit: 15,
                    },
                }).then(function (exists) {
                    console.log(exists);
                    var rs = _.map(exists, function (r) {
                        return r;
                    });
                    response(rs.sort());
                });
            
        },
        select: function (ev, ui) {
            $input.val(ui.item.label);
            // $input.next().val(ui.item.value);
            return false;
        },
        change: function( ev, ui ) {
            // console.log(ev,ui);
            if (!ui.item){
                $input.val('');
                $input.next().val('');
            }
        },
        autoFocus: true,
    });
}

/**
 * Allows the given input to propose existing website URLs.
 *
 * @param {ServicesMixin|Widget} self - an element capable to trigger an RPC
 * @param {jQuery} $input
 */
function autocompleteRegion(self, $input) {
    $input.autocomplete({
        source: function (request, response) {
            return self._rpc({
                    model: 'res.region',
                    method: 'search_record',
                    args: [null, request.term],
                    kwargs: {
                        limit: 15,
                    },
                }).then(function (exists) {
                    console.log(exists);
                    var rs = _.map(exists, function (r) {
                        return r;
                    });
                    response(rs.sort());
                });
            
        },
        select: function (ev, ui) {
            $input.val(ui.item.label);
            // $input.next().val(ui.item.value);
            return false;
        },
        change: function( ev, ui ) {
            // console.log(ev,ui);
            if (!ui.item){
                $input.val('');
                $input.next().val('');
            }
        },
        autoFocus: true,
    });
}

return {
    autocompleteCountry: autocompleteCountry,
    autocompleteBrgy: autocompleteBrgy,
    autocompleteCityMun: autocompleteCityMun,
    autocompleteProvince: autocompleteProvince,
    autocompleteRegion: autocompleteRegion,

};
});
