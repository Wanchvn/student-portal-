/**
 * Main JavaScript - shared utilities
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(#statusAlert)');
    alerts.forEach((alert) => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
