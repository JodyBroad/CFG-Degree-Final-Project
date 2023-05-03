document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sleep-form');
    const dateInput = document.getElementById('date-input');
    const hoursSleptInput = document.querySelector('input[name="hours-slept"]:checked');
    const sleepQualitytInput = document.querySelector('input[name="sleep-quality"]:checked');
    
    const saveEntry = async (event) => {
        event.preventDefault();
        const sleepData = {
            entryDate: dateInput.value,
            sleepQuality: sleepQualitytInput.value,
            hoursSlept: hoursSleptInput.value,
        };
        console.log(sleepData);
        // to do - integrate with flask
        const response = await fetch({
            url: 'http://localhost:5000/api/sleep-tracker/log-sleep',
            method: 'POST', 
            body: sleepData,
        });
    };
    
    form.addEventListener('submit', saveEntry);
    
});
