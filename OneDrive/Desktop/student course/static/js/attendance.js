/**
 * Attendance functionality for the course management system
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the attendance chart if present
    initializeAttendanceChart();
    
    // Setup the attendance form submission handler
    setupAttendanceForm();
});

/**
 * Initialize the attendance chart using Chart.js
 */
function initializeAttendanceChart() {
    const chartElement = document.getElementById('attendanceChart');
    if (!chartElement) return;
    
    const ctx = chartElement.getContext('2d');
    
    // Get the attendance data from the data attribute
    const attendanceDataStr = chartElement.getAttribute('data-attendance');
    if (!attendanceDataStr) return;
    
    try {
        const attendanceData = JSON.parse(attendanceDataStr);
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: attendanceData.dates,
                datasets: [{
                    label: 'Present',
                    data: attendanceData.present_counts,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (e) {
        console.error('Error initializing chart:', e);
    }
}

/**
 * Setup attendance form submission via AJAX
 */
function setupAttendanceForm() {
    const form = document.getElementById('attendanceForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Attendance marked successfully!');
                location.reload();
            } else {
                alert('Error marking attendance: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error marking attendance');
        });
    });
}
