document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sleep-form');
    const dateInput = document.getElementById('date-input');
    const hoursSleptInput = document.querySelector('input[name="hours-slept"]:checked');
    const sleepQualitytInput = document.querySelector('input[name="sleep-quality"]:checked');
    
    const today = new Date();
    dateInput.valueAsDate = today;
    dateInput.max = today.toISOString().split('T')[0];
    // setting as today's date
    // https://stackoverflow.com/questions/6982692/how-to-set-input-type-dates-default-value-to-today
    // https://stackoverflow.com/questions/32378590/set-date-input-fields-max-date-to-today


    const saveEntry = async (event) => {
        event.preventDefault();
        const sleepData = {
            entryDate: dateInput.value,
            sleepQuality: sleepQualitytInput.value,
            hoursSlept: hoursSleptInput.value,
        };
        console.log(sleepData);
        // to do - error handling
        await fetch('/api/sleep-tracker/log-sleep', {
            headers: {'Content-Type': 'application/json'},
            method: 'POST', 
            body: JSON.stringify(sleepData),
        });
    };
    
    form.addEventListener('submit', saveEntry);
    
});