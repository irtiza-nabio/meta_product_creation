/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ProductSelection = publicWidget.Widget.extend({
    selector: '.product-checkbox-wrapper',

    events: {
        'change .product-checkbox': 'updateTotal',
    },

    start: function () {
        this._super.apply(this, arguments);
        console.log("Product selection JS initialized!");
        this.totalDisplayWrapper = document.getElementById('total-points-display');
        this.totalDisplayValue = document.getElementById('total-points');

        // Initial setup
        if (this.totalDisplayWrapper && this.totalDisplayValue) {
            this.totalDisplayWrapper.style.display = 'none';
            this.totalDisplayValue.textContent = '0';
            this.updateTotal(); // In case some checkboxes are already selected
        }
    },

    updateTotal: function () {
        let totalPoints = 0;
        const checkboxes = this.el.querySelectorAll('.product-checkbox');

        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                totalPoints += 10;
            }
        });

        if (this.totalDisplayWrapper && this.totalDisplayValue) {
            if (totalPoints > 0) {
                this.totalDisplayWrapper.style.display = 'block';
                this.totalDisplayValue.textContent = totalPoints;
            } else {
                this.totalDisplayWrapper.style.display = 'none';
                this.totalDisplayValue.textContent = '0';
            }
        }
    },
});
