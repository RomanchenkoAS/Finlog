var table = document.getElementById('logTable');

// Proper format for money values
function formatter(value, currency) {
    // Set currency icon before number
    let currencyIcon = document.createElement('img');
    let path = `/static/log/icons/currency/${currency}.svg`
    currencyIcon.src = path;
    currencyIcon.width = '16';
    currencyIcon.height = '16';
    currencyIcon.style.verticalAlign = 'text-bottom';

    let currencyFormatter = new Intl.NumberFormat('en-US', {
        // Digits after ','
        minimumFractionDigits: 0,
    });

    return currencyIcon.outerHTML + ' ' + currencyFormatter.format(value);
}

// Load content from the /load_content/ url -- used on window load -- includes recusrive_render & scroll_down
function load_content(t) {

    fetch(`/load_content/?t=${t}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Not ok response');
            }
            return response.json();
        })
        .then(data => {
            recusrive_render(data.entries);
            scroll_down();
        })
        .catch(error => {
            console.error('Issue with fetch operation: ', error);
            alert('Server responded with 400')
        });
};

// Recursive rendering 
function recusrive_render(arr) {
    // Pick out the last item 
    var lastItem = arr.pop();

    // Base case
    if (typeof lastItem === 'undefined') {
        return 0
    } else {
        // Render this one
        add_row(lastItem, 'top');
        // Go deeper 'v'
        recusrive_render(arr);
    }
}

// Rendering just one row in the table (at the top of it for position=='top' and at the bottom for 'bottom')
function add_row(lastItem, position) {
    if (position == 'top') {
        var newrow = table.insertRow(0);
    } else if (position == 'bottom') {
        var newrow = table.insertRow();
    } else {
        console.error(`Invalid function call argument: ${position}`);
    }

    // Cells variables
    var cellValue = newrow.insertCell(0);
    var cellCategory = newrow.insertCell(1);
    var cellDate = newrow.insertCell(2);
    var cellComment = newrow.insertCell(3);
    var cellDelButton = newrow.insertCell(4);

    // Populate the cells
    cellValue.innerHTML = formatter(lastItem.value, lastItem.currency);
    cellCategory.innerHTML = lastItem.category;

    // Set local time
    // create a new Date object from the UTC string
    const utcDatetime = new Date(lastItem.datetime);
    const isoDatetimeString = utcDatetime.toISOString();

    // get the local datetime string using toLocaleString()
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const localDatetimeString = utcDatetime.toLocaleString([], { timeZone: timeZone, hourCycle: "h12" });

    const dateObj = new Date(isoDatetimeString);
    const formattedDate = dateObj.toLocaleString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: '2-digit'
    }).replace(',', '');

    cellDate.innerHTML = formattedDate;

    // Comment is ellipis (...) if empty
    if (lastItem.comment == '') {
        cellComment.innerHTML = '...';
    } else {
        cellComment.innerHTML = lastItem.comment;
    }

    // Create a new button element
    var deleteButton = document.createElement('button');

    // Set the button's attributes
    deleteButton.type = 'button';
    deleteButton.className = 'btn delete';
    deleteButton.id = lastItem.position + '-remove';
    deleteButton.onclick = function () { deleteEntry(lastItem.position); };

    let x_icon = document.createElement('img');
    x_icon.className = 'icon_button cross'
    x_icon.src = "/static/log/icons/cross.svg";

    deleteButton.appendChild(x_icon);

    // Append the button element to the cellDelButton cell
    cellDelButton.appendChild(deleteButton);

    newrow.style.backgroundColor = lastItem.color;

    newrow.id = lastItem.position;
};

// Manually (first - showing and then) scrolling down the table
function scroll_down() {
    var tableContainer = document.getElementById("logTableContainer");
    tableContainer.style.visibility = "visible";
    tableContainer.scrollTop = tableContainer.scrollHeight;
    tableContainer.style.scrollBehavior = "smooth";
};

// Featuring fetch
// Script to delete an entry with given entry.position
function deleteEntry(pos) {
    let t = document.getElementById('period_label').dataset.period;
    console.log(`fetching /remove/${pos}?t=${t}`);
    fetch(`/remove/${pos}?t=${t}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/JSON'
        },
        body: JSON.stringify({
            position: pos
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Not ok response');
            }
            return response.json();
        })
        .then(data => {

            // Received variables
            budget = data.budget.budget;
            spent = data.budget.spent;
            percent = data.budget.percent;
            currency = data.budget.currency;

            // Set info inside settings window
            budget_label.textContent = budget.toFixed(0);
            currency_label.textContent = currency;

            // Set budget
            set_budget(budget, spent, percent, currency);

            // Now actually remove from the page
            var row = document.getElementById(`${pos}`)
            row.remove();

            // Replace id's for rows & delete buttons
            let rows = table.childNodes[0].childNodes
            rows.forEach((item, index) => {
                let delete_button = document.getElementById(`${item.id}-remove`);
                // Change delete button id and behaviour
                delete_button.id = `${index}-remove`;
                delete_button.onclick = function () { deleteEntry(index); };
                // Change actual id
                item.id = index;
            })
        })
        .catch(error => {
            console.error('Issue with fetch operation: ', error);
        });
};


// Set budget value (when budget is changed - on modification of settings)
function set_budget(newbudget, spent, percent, currency) {
    // Cast values to number
    newbudget = Number(newbudget);
    spent = Number(spent);
    percent = Number(percent);

    let progressBar = document.getElementById("budget_progress");
    let progressDiv = document.getElementById("budget_progress_div");

    // Update progressBar
    progressBar.style.width = `${percent}%`;
    // Save newbudget on the page
    progressDiv.setAttribute('aria-valuemax', newbudget);
    progressDiv.setAttribute('aria-valuenow', spent);

    let budgetLabel = document.getElementById("budget");
    budgetLabel.textContent = Math.round(newbudget);

    let currencyLabel = document.getElementById("currency");
    currencyLabel.textContent = currency;

    let spentLabel = document.getElementById("spent");
    spentLabel.textContent = Math.round(spent);

    budget_icon = document.getElementById('budget_icon');
    if (percent >= 100) {
        budget_icon.src = "/static/log/icons/budget_overflow.svg";
    } else if (percent < 100) {
        budget_icon.src = "/static/log/icons/budget.svg";
    }

    progressBar.classList.remove(progressBar.classList[progressBar.classList.length - 1]);

    if (percent < 50) {
        progressBar.classList.add('bg-info');
    } else if (percent < 75) {
        progressBar.classList.add('bg-warning');
    } else {
        progressBar.classList.add('bg-danger');
    }
}


// Adding a new entry
$('#add-entry').on("submit", function (event) {
    event.preventDefault();

    // Get the form data and send an AJAX request to the server
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    value = document.getElementById('input-value').value;
    $.ajax({
        url: 'add',
        type: 'POST',
        headers: {
            'X-Timezone': timezone
        },
        data: $(this).serialize(),
        success: function (data) {
            // update the list on the page with the new data
            var newItem = data.entries[data.entries.length - 1];
            // Add it to the bottom of the table
            add_row(newItem, 'bottom');
            clear_form();
            scroll_down();

            // Received variables
            budget = data.budget.budget;
            spent = data.budget.spent;
            percent = data.budget.percent;
            currency = data.budget.currency;

            // Set budget
            set_budget(budget, spent, percent, currency);
        },
        error: function () {
            alert(`Error adding entry. Sent data: ${this}`);
        }
    });
});

// Function to clear add-entry-form
function clear_form() {
    const valueInput = document.getElementById("input-value");
    const categorySelect = document.getElementById("input-category");
    const commentInput = document.getElementById("input-comment");

    // Clear the input fields
    valueInput.value = "";
    commentInput.value = "";

    // Set the select element to its default value
    categorySelect.selectedIndex = 0;
};

// Delete all rows from table
function clear_table() {
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
}


// Function to swap between log for All/Day/Month
function cycle() {
    let label = document.getElementById('period_label');
    index = label.dataset.index;
    index++;

    // For actual cycling
    if (index == 3) {
        index = 0;
    }

    clear_table();

    if (index == 0) {
        label.textContent = 'All latest';
        label.dataset.period = 'all';
        load_content('all');
    } else if (index == 1) {
        label.textContent = 'Today';
        label.dataset.period = 'day';
        load_content('day');
    } else if (index == 2) {
        label.textContent = 'This month';
        label.dataset.period = 'month';
        load_content('month');
    }

    label.dataset.index = index;
}

// Swap visibility of budget progress-bar
function progress() {
    let budget = document.getElementById("budget_container")

    if (budget.style.display == 'flex') {
        budget.style.display = 'none';
    } else {
        budget.style.display = 'flex';
    };
};



window.onload = function () {
    // On loading window call function to load entries from server & render them on the page
    // All refers to 'load all entries'
    load_content('all');
};