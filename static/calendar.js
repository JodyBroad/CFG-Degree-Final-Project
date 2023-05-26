document.addEventListener('DOMContentLoaded', () => {
    const selectedUserControl = document.getElementById('selected-user');
    const selectedMetricControl = document.getElementById('selected-metric');

    const today = new Date().setHours(0);

    const emojiMap = {
        "": "😶",
        "Happy": "😁",
        "Sad": "😢",
        "Angry": "😠",
        "Sleepy": "😪",
    };

    const buildMoodEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: emojiMap[data.mood],
        classNames: ['emoji'],
    });

    const buildSleepDurationEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.sleepDuration}`,
    });

    const buildSleepQualityEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.sleepQuality}`,
    });

    const buildStepsTakenEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.steps} Steps`,
    });

    const buildWaterEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.water}ml`,
        classNames: ['fc-day-future', 'fc-day-other']
    });

    const getEventsForUser = () => {
        const user = users.find(user => user.userId.toString() === selectedUserControl.value);
        let buildFunction;

        switch (selectedMetricControl.value) {
            case 'Mood':
                buildFunction = buildMoodEvent;
                break;
            case 'Sleep Duration':
                buildFunction = buildSleepDurationEvent;
                break;
            case 'Sleep Quality':
                buildFunction = buildSleepQualityEvent;
                break;
            case 'Water Consumption':
                buildFunction = buildWaterEvent;
                break;
            case 'Steps Taken':
                buildFunction = buildStepsTakenEvent;
                break;
            default:
                buildFunction = buildMoodEvent;
                break;
        }

        const entries = user.entries.map(data => buildFunction(data, {
            start: new Date(data.date),
            allDay: true,
            display: 'background',
        })) ?? [];

        const uniqueEvents = entries.reduce((accumulator, current) => {
            current.start = current.start.setHours(0);

            if (!accumulator.find((item) => item.start == current.start)) {
              accumulator.push(current);
            }

            return accumulator;
          }, []);

        return uniqueEvents;
    };

    const onDateClick = (event) => {
        if (event.date > today) {
            // Ignore future dates
            return;
        }

        // Navigate to the tracking page with the date as a query string
        window.location = `/tracking?date=${event.date.toLocaleDateString()}`;
    };

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        eventColor: "rgb(0, 0, 0, 0)",
        eventBorderColor: "rgb(0, 0, 0, 0)",
        initialView: 'dayGridMonth',
        fixedWeekCount: false,
        firstDay: 1,
        events: getEventsForUser(),
        dateClick: onDateClick,
        dayCellClassNames: ({ isFuture }) => isFuture ? ['fc-day-other'] : [],
    });

    const resetCalendarEvents = (event) => {
        calendar.getEventSources().forEach(src => src.remove());
        calendar.addEventSource(getEventsForUser(event.target.value));
    }

    selectedUserControl.addEventListener('change', resetCalendarEvents);
    selectedMetricControl.addEventListener('change', resetCalendarEvents);
    calendar.render();
});
