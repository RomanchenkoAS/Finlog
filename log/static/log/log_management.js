var table = document.getElementById('logTable');

// Proper format for money values
function formatter(value, currency) {
    // implementation
    let currencyFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
    });

    return currencyFormatter.format(value);
}

// Load content from the /load_content/ url -- used on window load -- includes recusrive_render & scroll_down
function load_content() {
    fetch(`/load_content/`)
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
        });
};

// Recursive rendering 
function recusrive_render(arr) {
    // Pick out the last item 
    var lastItem = arr.pop();

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
    cellCategory.innerHTML = lastItem.category_title;
    cellDate.innerHTML = lastItem.datetime;

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
    deleteButton.innerHTML = '&times;';

    // Append the button element to the cellDelButton cell
    cellDelButton.appendChild(deleteButton);

    // Obsolete TODO: remove
    // Making it of the right class 
    // newrow.classList.add(lastItem.category);

    // console.log(lastItem.category)
    // Setting a proper color instead of class:
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
    // console.log(`I am to delete an entry #${pos}`);

    fetch(`/remove/${pos}/`, {
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

            row.style['display'] = 'none'
        })
        .catch(error => {
            console.error('Issue with fetch operation: ', error);
        });

};

// Adding a new entry
$('#add-entry').on("submit", function (event) {
    event.preventDefault();
    // console.log($(this).serialize());
    // Get the form data and send an AJAX request to the server
    $.ajax({
        url: 'add',
        type: 'POST',
        data: $(this).serialize(),
        success: function (data) {
            // update the list on the page with the new data
            var newItem = data.entries[data.entries.length - 1];
            // Add it to the bottom of the table
            add_row(newItem, 'bottom');
            clear_form();
            scroll_down();
        },
        error: function () {
            alert(`Error adding entry. Sent data: ${$(this).serialize}`);
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

window.onload = function () {
    load_content();
    // console.log('i do work')
};