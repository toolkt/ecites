odoo.define("ecites.registration", function (require) {
  "use strict";

  var core = require("web.core");
  var publicWidget = require("web.public.widget");
  var myUtils = require("ecites.utils");
  var _t = core._t;

  console.log("Registration Loaded");


  publicWidget.registry.RegistrationForm = publicWidget.Widget.extend({
    selector: "#ecites_registration_form",

    events: {
      // "change #image2_1920": "_onFileImage21920Change",
      // "click #submit-reg-step-1-button": "_onSubmitReg1FormButton",
      "change #country_id": "_onChangeCountry",
    },

    init: function () {
      this._super.apply(this, arguments);
    },
    start: function (editable_mode) {
      if (editable_mode) {
        this.stop();
        return;
      }
      var self = this;
      myUtils.autocompleteBrgy(this, this.$('input[name="brgy"]'));
      myUtils.autocompleteCityMun(this, this.$('input[name="citymun"]'));
      myUtils.autocompleteProvince(this, this.$('input[name="province"]'));
      myUtils.autocompleteRegion(this, this.$('input[name="region"]'));

      myUtils.autocompleteBrgy(this, this.$('input[name="brgy_2"]'));
      myUtils.autocompleteCityMun(this, this.$('input[name="citymun_2"]'));
      myUtils.autocompleteProvince(this, this.$('input[name="province_2"]'));
      myUtils.autocompleteRegion(this, this.$('input[name="region_2"]'));

    },
    destroy: function () {
      this._super.apply(this, arguments);
    },

    _onChangeCountry: function (e){
      var self = this;
      console.log(e);
      console.log(this.$("#country_id").val());
    }
  });
});


