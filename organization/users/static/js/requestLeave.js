button = document.getElementById('submitbutton')
numberofdays_field = document.getElementById('numberofdays')
button.addEventListener('click', (e) => {
    from_date = document.getElementById('from_date').value
    to_date = document.getElementById('to_date').value
    from_day = from_date.split('-')
    to_day = to_date.split('-')
    calculated_number_of_day = parseInt(to_day[2]) - parseInt(from_day[2])
    calculated_number_of_day += 1
    numberofdays_field.value = calculated_number_of_day
})
