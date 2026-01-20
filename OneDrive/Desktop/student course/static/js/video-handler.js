/**
 * Video handler for course detail page
 * Handles YouTube video loading errors and provides fallback
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get all video containers
    const videoContainers = document.querySelectorAll('.collapse');
    
    // Add event listeners for when videos are shown
    videoContainers.forEach(container => {
        container.addEventListener('shown.bs.collapse', function() {
            // Find the iframe in this container
            const iframe = this.querySelector('iframe');
            if (iframe) {
                // Check if the iframe is loaded correctly
                checkVideoLoaded(iframe);
            }
        });
    });
    
    // Function to check if video is loaded
    function checkVideoLoaded(iframe) {
        // Set a timeout to check if the video loaded
        setTimeout(() => {
            try {
                // Try to access the iframe content - if blocked by CORS, the video is probably loading fine
                // If we can access it, there might be an error
                const iframeContent = iframe.contentWindow.document;
                
                // If we got here, there's likely an error
                showVideoError(iframe);
            } catch (e) {
                // CORS error means the video is probably loading correctly
                // This is normal for YouTube embeds
            }
        }, 2000);
    }
    
    // Function to show a video error
    function showVideoError(iframe) {
        const errorContainer = iframe.parentElement.nextElementSibling;
        if (errorContainer && errorContainer.classList.contains('video-error-container')) {
            errorContainer.classList.remove('d-none');
            iframe.style.display = 'none';
        }
    }
    
    // Add manual refresh button for videos
    const refreshButtons = document.querySelectorAll('.refresh-video');
    refreshButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const videoId = this.dataset.videoId;
            const iframe = document.querySelector(`#video-${videoId} iframe`);
            if (iframe) {
                // Reload the iframe
                const src = iframe.src;
                iframe.src = '';
                setTimeout(() => {
                    iframe.src = src;
                }, 100);
                
                // Hide any error messages
                const errorContainer = iframe.parentElement.nextElementSibling;
                if (errorContainer) {
                    errorContainer.classList.add('d-none');
                    iframe.style.display = 'block';
                }
            }
        });
    });
});
