document.addEventListener('DOMContentLoaded', () => {
    const selectedUserControl = document.getElementById('selected-user');
    const selectedMetricControl = document.getElementById('selected-metric');

    const emojiMap = {
        "": "😶",
        "Happy": "😀",
        "Sad": "😢",
        "Angry": "🤬",
        "Sleepy": "😴",
        "Sick": "🤒",
        "Anxious": "😟",
    };

    const getWaterImage = (waterConsumption) => {
        if (waterConsumption < 1000) {
            return '/static/images/water/1.png';
        } else if (waterConsumption >= 1000 && waterConsumption <= 2000) {
            return '/static/images/water/2.png';
        } else {
            return '/static/images/water/3.png'
        }
    }

    const buildMoodEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: emojiMap[data.mood],
        classNames: ['emoji'],
        type: 'Mood',
    });

    const buildSleepDurationEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.sleepDuration}`,
        type: 'Sleep Duration',
    });

    const buildSleepQualityEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.sleepQuality}`,
        type: 'Sleep Quality',
    });

    const buildStepsTakenEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.steps} Steps`,
        type: 'Steps Taken',
    });

    const buildWaterEvent = (data, baseEvent) => ({
        ...baseEvent,
        title: `${data.water}ml`,
        classNames: ['fc-day-future', 'fc-day-other'],
        imageUrl: getWaterImage(data.water),
        type: 'Water Consumption',
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

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        eventColor: "rgb(0, 0, 0, 0)",
        eventBorderColor: "rgb(0, 0, 0, 0)",
        initialView: 'dayGridMonth',
        fixedWeekCount: false,
        firstDay: 1,
        events: getEventsForUser(),
        dayCellClassNames: ({ isFuture }) => isFuture ? ['fc-day-other'] : [],
        eventContent: (arg) => {
            switch (arg.event.extendedProps.type) {
                case 'Water Consumption':
                    return {
                        html: `
                        <div class="water-consumption-cell">
                            <img src="${arg.event.extendedProps.imageUrl}" />
                            <p>${arg.event.title}</p>
                        </div>
                        `
                    }
                default:
                    return {
                        html: `<div class="fc-event-title">${arg.event.title}</div>`
                    };
            }
        }
    });

    const resetCalendarEvents = (event) => {
        calendar.getEventSources().forEach(src => src.remove());
        calendar.addEventSource(getEventsForUser(event.target.value));
    }

    selectedUserControl.addEventListener('change', resetCalendarEvents);
    selectedMetricControl.addEventListener('change', resetCalendarEvents);
    calendar.render();
});
