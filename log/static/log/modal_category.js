// Interactive colorpickers
var colorPickers = document.getElementsByClassName("color_picker");

for (var i = 0; i < colorPickers.length; i++) {
    colorPickers[i].addEventListener('input', function () {
        // Take this color
        let colorCode = this.value;
        // Get corresponding category by cutting off '-colorpicker'
        let category = this.id.substring(0, this.id.indexOf('-colorpicker'));
        // Get corresponding item and set it's color to the picked one
        let item = document.getElementById(`${category}-item`);

        // Also change all the relevant itmes to a new color
        item.style.backgroundColor = colorCode;

        // All cells
        const cells = document.querySelectorAll("td");
        // All cells with category written there
        const cellsToChange = Array.from(cells).filter(cell => cell.textContent.includes(category));

        // And then changing their parent's color 
        cellsToChange.forEach(item => {
            item.parentElement.style.backgroundColor = colorCode;
        });
    });
};


// Script for collapsible headers 
var coll = document.getElementsByClassName("collapsible");

for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        };

        // Set color for colorpickers
        var colorPickers = content.querySelectorAll('.color_picker');

        colorPickers.forEach(element => {
            let parent = element.parentNode.parentNode;
            let color = getComputedStyle(parent).getPropertyValue('background-color');
            element.value = rgbToHex(color);
        });
    });
};

// Show 'custom' collapsible header 
var custom = document.getElementById("collapsible_custom");
var customHeaderContent = custom.nextElementSibling;

function expand_custom() {
    custom.classList.toggle("active");
    if (customHeaderContent.style.maxHeight) {
        customHeaderContent.style.maxHeight = null;
    } else {
        customHeaderContent.style.maxHeight = customHeaderContent.scrollHeight + "px";
    };
};


// Transforms from rgb(x, y, z) into hexadecimal
function rgbToHex(rgb) {
    var components = rgb.match(/\d+/g);
    var hex = '#';
    for (var i = 0; i < 3; i++) {
        var component = parseInt(components[i]).toString(16);
        hex += component.length == 1 ? '0' + component : component;
    };
    return hex;
};

// Show relevant edit palette on edit <a> click || hide edit button 
function expand(input_category) {
    document.getElementById(input_category + "-edit-button").style.display = 'none';
    document.getElementById(input_category + "-edit").style.display = 'inline-block';
};
// Hide edit palette
function hide(input_category) {
    document.getElementById(input_category + "-edit").style.display = 'none';
    document.getElementById(input_category + "-edit-button").style.display = 'flex';

    let paragraph = document.getElementById(input_category + "-item");
    let previousColor = paragraph.dataset.color;
    let color_picker = document.getElementById(input_category + "-colorpicker");

    color_picker.value = previousColor;
    paragraph.style.backgroundColor = previousColor;

    // Also change all the relevant itmes to the previous color

    // All cells
    const cells = document.querySelectorAll("td");
    // All cells with category written there
    const cellsToChange = Array.from(cells).filter(cell => cell.textContent.includes(input_category));

    // And then changing their parent's color 
    cellsToChange.forEach(item => {
        item.parentElement.style.backgroundColor = previousColor;
    });

};

// Variable that controls behaviour of the page after closing the modal window
let called_action = 'none';

// Action options: edit | add | delete | reset
function edit(input_category, action = 'edit') {
    // Find corresponding colorpicker
    let colorPicker = document.getElementById(input_category + "-colorpicker");

    // Color that is set on the corresponding colorpicker
    color = colorPicker.value;

    // Find name input field
    let name_input = document.getElementById(`${input_category}-newname`);

    // Error handling
    if (name_input != null) {
        newname = name_input.value;
    } else {
        newname = input_category;
    };

    // If name is different, operation marked as 'rename'
    if (newname != input_category && action == 'edit') {
        action = 'rename';
    };

    console.log(`${action} ${input_category} | new color: ${colorPicker.value} | |new name: ${newname} | sending xhr request`);

    // Send actual request at /edit/
    var xhr = new XMLHttpRequest();
    var url = "/edit/";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Simple ok response
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 204) {
            console.log("Request successful");

            // Called action is a global variable, it needs to get data for further use
            called_action = action;

            // If there was a new category added, spawn it right there
            if (action == 'add') {
                let container = document.getElementById("custom_categories_container");
                let newSpan = document.createElement("span");
                let newParagraph = document.createElement("p");

                newParagraph.textContent = newname;
                newParagraph.style.backgroundColor = color;
                newParagraph.className = 'category small-margin';

                newSpan.appendChild(newParagraph);

                let index = container.children.length - 1;
                let previousParagraph = container.children[index];
                container.insertBefore(newSpan, previousParagraph);

                // Expand the header to contain one more line
                customHeaderContent.style.maxHeight = customHeaderContent.scrollHeight + "px";

                var content = custom.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                };
            };

            if (action == 'delete') {
                deleted = document.getElementById(`${name}-item`)
                // Yeah looks weird, works though
                deleted.parentElement.removeChild(deleted);
            };

            if (action == 'rename') {
                // Change existing category inside modal window
                document.getElementById(`${name}-item`).textContent = newname;

                // Change category name for entries
                // All cells
                const cells = document.querySelectorAll("td");
                // All cells with category written there
                const cellsToChange = Array.from(cells).filter(cell => cell.textContent.includes(name));

                // And then changing text wtitten there
                cellsToChange.forEach(item => {
                    item.textContent = newname;
                });

                // Change category name in select
                const select = document.querySelectorAll("option");
                const selectToChange = Array.from(select).filter(select => select.value.includes(name));
                selectToChange[0].value = newname;
                selectToChange[0].textContent = newname;

            };

            if (action == 'reset') {
                location.reload();
            }
        } else if (xhr.status === 400) {
            alert(`Error at editing the category ${input_category} | ${action}`);
        };
    };

    // Sending data
    var data = JSON.stringify({ "name": input_category, "color": color, "action": action, "newname": newname });
    xhr.send(data);

    // Set data value of <p> to new color
    let p = document.getElementById(input_category + '-item')
    p.dataset.color = color;

    // Hide edit palette
    hide(input_category);

};

// Dissmiss all the changes on closing the modal
var categoriesModal = document.getElementById("categoriesModal");

categoriesModal.addEventListener("hidden.bs.modal", function () {

    // If a new category was added - refresh the page
    if (called_action == 'add' || called_action == 'delete' || called_action == 'rename') {
        location.reload();
    } else {
        // If the page doesnt reload, run mass hide for all relevant <p> items
        // Get all the p | all p with category there | all p except add-item | hide palette for them
        let p = document.querySelectorAll('p')
        let p_categories = Array.from(p).filter(node => node.id.includes('-item'));

        p_categories.forEach(item => {
            if (item.id != 'add-item') {
                let category = item.id.slice(0, item.id.indexOf('-item'));
                hide(category);
            };
        });

    };
});

// Event listeners for space/enter on category name input
const inputField = document.getElementsByClassName('change_name');
for (let i = 0; i < inputField.length; i++) {
    inputField[i].addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
            event.preventDefault();
        };

        if (event.code === 'Enter') {

            if (inputField[i].id == 'add-newname') {
                edit("add", "add");
            } else {
                // Cut off category part from the string
                let category = inputField[i].id.slice(0, inputField[i].id.indexOf('-newname'));
                edit(category, "edit");
            };
        };
    });
};