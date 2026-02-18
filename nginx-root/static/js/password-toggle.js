// Password visibility toggle for all password fields
// Automatically enhances password inputs with show/hide functionality

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // Find all password input fields
        var passwordFields = document.querySelectorAll('input[type="password"]');

        if (!passwordFields.length) {
            return;
        }

        passwordFields.forEach(function(field) {
            // Skip if already enhanced or if it's a honeypot field
            if (field.dataset.toggleEnhanced || field.closest('[style*="left: -9999px"]')) {
                return;
            }

            field.dataset.toggleEnhanced = 'true';

            // Create wrapper div for positioning
            var wrapper = document.createElement('div');
            wrapper.style.position = 'relative';
            wrapper.style.display = 'block';

            // Wrap the input field
            field.parentNode.insertBefore(wrapper, field);
            wrapper.appendChild(field);

            // Create the toggle checkbox and label
            var toggleContainer = document.createElement('div');
            toggleContainer.style.marginTop = '5px';
            toggleContainer.style.marginBottom = '10px';

            var toggleId = 'show-password-' + Math.random().toString(36).substr(2, 9);

            var checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = toggleId;
            checkbox.style.marginRight = '6px';
            checkbox.style.cursor = 'pointer';

            var label = document.createElement('label');
            label.htmlFor = toggleId;
            label.style.fontWeight = 'normal';
            label.style.cursor = 'pointer';
            label.style.fontSize = '0.9em';
            label.style.color = '#666';
            label.textContent = 'Show password';

            toggleContainer.appendChild(checkbox);
            toggleContainer.appendChild(label);
            wrapper.appendChild(toggleContainer);

            // Toggle password visibility
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    field.type = 'text';
                    label.textContent = 'Hide password';
                } else {
                    field.type = 'password';
                    label.textContent = 'Show password';
                }
            });
        });
    });
})();
