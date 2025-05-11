// app.js - Client-side functionality for Exam Scheduler

document.addEventListener('DOMContentLoaded', function() {
    
    // Form validation
    const schedulerForm = document.getElementById('scheduler-form');
    if (schedulerForm) {
        schedulerForm.addEventListener('submit', function(event) {
            const subjectsInput = document.getElementById('subjects');
            const studentsInput = document.getElementById('students');
            
            // Validate subjects
            if (!subjectsInput.value.trim()) {
                event.preventDefault();
                alert('Please enter at least one subject.');
                subjectsInput.focus();
                return;
            }
            
            // Validate students
            if (!studentsInput.value.trim()) {
                event.preventDefault();
                alert('Please enter student enrollment information.');
                studentsInput.focus();
                return;
            }
            
            // Check format of student data
            const lines = studentsInput.value.trim().split('\n');
            for (const line of lines) {
                if (!line.includes(':')) {
                    event.preventDefault();
                    alert('Invalid student format. Please use "Student: Subject1, Subject2" format.');
                    studentsInput.focus();
                    return;
                }
            }
        });
    }
    
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add highlighting effect to table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.classList.add('table-active');
        });
        row.addEventListener('mouseleave', () => {
            row.classList.remove('table-active');
        });
    });
});
