// Close Call Database - Navbar Active Page Detection
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
});