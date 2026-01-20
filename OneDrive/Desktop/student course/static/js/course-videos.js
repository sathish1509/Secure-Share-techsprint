/**
 * Course Videos Functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Handle video sharing
    const shareButtons = document.querySelectorAll('.share-video');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const videoId = this.getAttribute('data-video-id');
            const shareUrl = `https://www.youtube.com/watch?v=${videoId}`;
            
            // Check if Web Share API is supported
            if (navigator.share) {
                navigator.share({
                    title: 'Check out this course video',
                    text: 'I found this helpful video from my course',
                    url: shareUrl
                }).then(() => {
                    console.log('Shared successfully');
                }).catch((error) => {
                    console.error('Error sharing:', error);
                    fallbackShare(shareUrl);
                });
            } else {
                fallbackShare(shareUrl);
            }
        });
    });
    
    function fallbackShare(url) {
        // Create temp input to copy URL
        const tempInput = document.createElement('input');
        document.body.appendChild(tempInput);
        tempInput.value = url;
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        
        // Show alert
        alert('Video URL copied to clipboard: ' + url);
    }
    
    // Handle video refresh
    const refreshButtons = document.querySelectorAll('.refresh-video');
    refreshButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation(); // Prevent collapse toggle
            
            const videoId = this.getAttribute('data-video-id');
            const videoContainer = document.querySelector(`#video-${videoId}`);
            
            if (videoContainer) {
                const iframe = videoContainer.querySelector('iframe');
                if (iframe) {
                    // Reload iframe by refreshing src
                    const currentSrc = iframe.src;
                    iframe.src = '';
                    setTimeout(() => {
                        iframe.src = currentSrc;
                    }, 100);
                    
                    // Show loading indicator
                    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                    setTimeout(() => {
                        this.innerHTML = '<i class="fas fa-sync-alt"></i>';
                    }, 1000);
                }
            }
        });
    });
    
    // Handle download notes button (placeholder functionality)
    const downloadButtons = document.querySelectorAll('.download-notes');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const videoId = this.getAttribute('data-video-id');
            alert(`Notes for video ${videoId} will be available soon!`);
        });
    });
    
    // Improve video error handling
    const videoIframes = document.querySelectorAll('.video-container iframe');
    videoIframes.forEach(iframe => {
        iframe.addEventListener('error', function() {
            const errorContainer = this.closest('.video-container').nextElementSibling;
            if (errorContainer && errorContainer.classList.contains('video-error-container')) {
                errorContainer.classList.remove('d-none');
            }
        });
    });
    
    // Video toggle buttons functionality
    const videoToggles = document.querySelectorAll('.video-toggle');
    videoToggles.forEach(button => {
        button.addEventListener('click', function() {
            // Change button text based on collapse state
            const targetId = this.getAttribute('data-bs-target');
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            if (isExpanded) {
                this.innerHTML = '<i class="fas fa-eye"></i> Watch';
            } else {
                this.innerHTML = '<i class="fas fa-eye-slash"></i> Hide';
            }
        });
    });
});
