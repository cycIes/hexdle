document.addEventListener('DOMContentLoaded', () => {
    let input = document.querySelector('#input');
    let fields = input.querySelectorAll('input');
    let not_forward_keys = ['Backspace', 'Shift', 'ArrowLeft', 'ArrowRight', 'Tab']

    fields.forEach((field) => field.addEventListener('keyup', (e) => {
        if (!(not_forward_keys.includes(e.key))) 
        {
            field.blur();
            next = field.nextElementSibling;
            if (next) 
            {
                next.focus();
            }
        }
    }));
    fields.forEach((field) => field.addEventListener('keydown', (e) => {
        if ((e.key === 'Backspace' && field.value === '') || e.key === 'ArrowLeft')
        {
            field.blur()
            previous = field.previousElementSibling
            if (previous)
            {
                previous.focus();
            }
        }
    }));
});
