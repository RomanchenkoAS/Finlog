var table = document.getElementById('logTable');

// Proper format for money values
function formatter(value, currency) {
    // Set currency 
    let currencyIcon = document.createElement('img');
    let path = `/static/log/icons/currency/${currency}.svg`
    currencyIcon.src = path;
    currencyIcon.width = '16';
    currencyIcon.height = '16';
    currencyIcon.style.verticalAlign = 'text-bottom';
    
    // currency = 'KE'
    let currencyFormatter = new Intl.NumberFormat('en-US', {
        // Digits after ','
        minimumFractionDigits: 0,
    });

    return currencyIcon.outerHTML + ' ' + currencyFormatter.format(value);
}
// Load content from the /load_content/ url -- used on window load -- includes recusrive_render & scroll_down
function load_content(t) {
    // console.log('load function')
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

    // console.log(lastItem);
    if (typeof lastItem === 'undefined') {
        // console.log('That was the last one :3')
        return 0
    } else {
        // Render this one
        // console.dir(lastItem)
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
    //cellValue.innerHTML     = `${lastItem.value} ${lastItem.currency}`;
    cellCategory.innerHTML = lastItem.category;

    // Set local time
    // create a new Date object from the UTC string
    const utcDatetime = new Date(lastItem.datetime);
    
    // get the local datetime string using toLocaleString()
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const localDatetimeString = utcDatetime.toLocaleString([], { timeZone: timeZone, hourCycle: "h23" });

    const dateObj = new Date(localDatetimeString);
    const formattedDate = dateObj.toLocaleString('en-US', {
        hour12: false,
        hour: 'numeric',
        minute: 'numeric',
        day: 'numeric',
        month: 'numeric',
        year: 'numeric'
      });
    
    // console.log(localDatetimeString); 
    cellDate.innerHTML = formattedDate;



    // Comment is ... if empty
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

// Script to delete an entry with given entry.position
function deleteEntry(pos) {
    console.log(`I am to delete an entry #${pos}`);
    let t = document.getElementById('period_label').dataset.period;;
    console.log(t);
    console.log(`/remove/${pos}?t=${t}`);
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
            // Now actually remove from the page
            var row = document.getElementById(`${pos}`)

            row.remove();

            // Replace id's for rows & delete buttons
            let rows = table.childNodes[0].childNodes
            rows.forEach((item, index) =>{
                let delete_button = document.getElementById(`${item.id}-remove`);
                // Change delete button id and behaviour
                delete_button.id = `${index}-remove`;
                delete_button.onclick = function () { deleteEntry(index); };
                // Change actual id
                item.id = index;
                // console.log(index)
                // console.log(item);
            })
        })
        .catch(error => {
            console.error('Issue with fetch operation: ', error);
        });

};

function update_budget(value) {
    let progressBar = document.getElementById("budget_progress");
    let progressDiv = document.getElementById("budget_progress_div");

    let budget = progressDiv.getAttribute('aria-valuemax');
    let spent = progressDiv.getAttribute('aria-valuenow');
    
    // Math
    spent = Number(spent) + value;
    let percent = (spent / budget);
    
    // Setting properties
    progressBar.style.width = `${percent * 100}%`;
    progressDiv.setAttribute('aria-valuenow', spent);
}

function set_budget(value) {
    let progressBar = document.getElementById("budget_progress");
    let progressDiv = document.getElementById("budget_progress_div");
    let spent = progressDiv.getAttribute('aria-valuenow');

    budget = value;
    let percent = (spent / budget);

    progressBar.style.width = `${percent * 100}%`;
    progressDiv.setAttribute('aria-valuemax', budget);
}


// Adding a new entry
$('#add-entry').on("submit", function (event) {
    event.preventDefault();
    // console.log($(this).serialize());
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
            // console.log(value);
            update_budget(value);
            
            
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

function clear_table() {
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
}



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

    console.log(budget.style.display)
    if (budget.style.display == 'flex') {
        //console.log('yeah it is')
        budget.style.display = 'none';
    } else {
        budget.style.display = 'flex';
    }
    console.log(budget.style.display)
}



window.onload = function () {
    // console.log('i do work')
    load_content('all');
};