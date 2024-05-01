entries = document.getElementById('entries')
entries.addEventListener('change', function() {
    // Store the selected value in local storage
    localStorage.setItem('selectedEntries', this.value);
});


// Retrieve the selected value from local storage
var selectedEntries = localStorage.getItem('selectedEntries');
if (selectedEntries) {
    // Set the selected value as the selected option
    document.getElementById('entries').value = selectedEntries;
}

const deleteDepartment = (id) => {
     // If the user confirms the deletion, send an AJAX request to the server
     $.ajax({
        url: `http://localhost:5000/delete_department/${id}`,
        success: function(response) {
            // Handle the success response, if needed
            console.log('deletion completed');
            location.reload();
        },
        error: function(xhr, status, error) {
            // Handle errors, if any
            console.error('xhr');
        }
    });
}

