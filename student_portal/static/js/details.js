/**
 * Student details page - AJAX admission status update
 */

document.addEventListener('DOMContentLoaded', () => {
    const statusForm = document.getElementById('statusForm');
    if (!statusForm) return;

    statusForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const studentId = statusForm.dataset.studentId;
        const statusSelect = document.getElementById('statusSelect');
        const updateBtn = document.getElementById('updateStatusBtn');
        const statusAlert = document.getElementById('statusAlert');
        const status = statusSelect.value;

        updateBtn.disabled = true;
        updateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Updating...';

        try {
            const response = await fetch(`/api/update-status/${studentId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                statusAlert.classList.remove('d-none');
                updateStatusBadge(status);

                setTimeout(() => {
                    statusAlert.classList.add('d-none');
                }, 4000);
            } else {
                alert(data.message || 'Failed to update status. Please try again.');
            }
        } catch (error) {
            console.error('Status update error:', error);
            alert('An error occurred while updating status.');
        } finally {
            updateBtn.disabled = false;
            updateBtn.textContent = 'Update Status';
        }
    });
});

/**
 * Update status badge on the page after successful AJAX update
 */
function updateStatusBadge(status) {
    const badges = document.querySelectorAll('.status-badge');
    badges.forEach((badge) => {
        badge.textContent = status;
        badge.className = `badge status-badge status-${status.toLowerCase()} fs-6`;
    });
}
