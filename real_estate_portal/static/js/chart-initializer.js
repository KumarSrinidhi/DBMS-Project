// Initialize chart when DOM is ready with optimized configuration
document.addEventListener('DOMContentLoaded', function() {
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') {
        console.error('Chart.js library is not loaded');
        return;
    }
    
    // Find the chart element
    const chartElement = document.getElementById('loanChart');
    if (!chartElement) return;
    
    // Get data from data attributes
    const principal = parseFloat(chartElement.dataset.principal) || 0;
    const interest = parseFloat(chartElement.dataset.interest) || 0;
    
    // Only create chart if we have valid data
    if (principal <= 0 && interest <= 0) return;
    
    // Use requestAnimationFrame for better performance
    requestAnimationFrame(function() {
        const ctx = chartElement.getContext('2d');
        
        // Create the chart with optimized configuration
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Principal Amount', 'Total Interest'],
                datasets: [{
                    data: [principal, interest],
                    backgroundColor: ['#2563eb', '#ef4444'],
                    borderColor: ['#ffffff', '#ffffff'],
                    borderWidth: 2,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                family: "'Poppins', sans-serif",
                                size: 14,
                                weight: 600
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                const label = context.label || '';
                                return label + ': ₹' + value.toLocaleString('en-IN');
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        });
    });
});
