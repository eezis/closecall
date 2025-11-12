// Close Call Database - Navbar Active Page Detection and Mobile Menu Collapse
document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    var currentPath = window.location.pathname;

    // Get all navbar links
    var navLinks = document.querySelectorAll('.navbar-nav > li > a');

    // Function to check if a link matches the current page
    function isActive(link) {
        var href = link.getAttribute('href');
        if (!href) return false;

        // Exact match
        if (href === currentPath) return true;

        // Handle home page
        if (currentPath === '/' && (href === '/home' || href === '/')) return true;
        if (currentPath === '/home' && (href === '/' || href === '/home')) return true;

        // Handle sections (e.g., /news/* matches /news)
        if (currentPath.startsWith(href + '/') && href !== '/') return true;

        return false;
    }

    // Apply active class to matching links
    navLinks.forEach(function(link) {
        if (isActive(link)) {
            link.parentElement.classList.add('active');
        }
    });

    // Mobile menu collapse functionality
    // Close the navbar when a link is clicked on mobile devices
    var navbarCollapse = document.querySelector('.navbar-collapse');
    var navbarToggle = document.querySelector('.navbar-toggle');

    if (navbarCollapse && navbarToggle) {
        // Get all clickable links in the navbar (including dropdown items)
        var allNavLinks = document.querySelectorAll('.navbar-collapse a');

        allNavLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                // Only collapse if navbar is currently expanded (on mobile)
                if (navbarCollapse.classList.contains('in')) {
                    // Use Bootstrap's collapse method if available, otherwise toggle manually
                    if (typeof jQuery !== 'undefined' && jQuery.fn.collapse) {
                        jQuery(navbarCollapse).collapse('hide');
                    } else {
                        navbarCollapse.classList.remove('in');
                    }
                }
            });
        });

        // Toggle collapse when hamburger is clicked (Bootstrap should handle this, but ensuring it works)
        navbarToggle.addEventListener('click', function() {
            if (typeof jQuery !== 'undefined' && jQuery.fn.collapse) {
                jQuery(navbarCollapse).collapse('toggle');
            }
        });
    }
});