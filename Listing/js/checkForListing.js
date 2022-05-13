let personnrList = [];

onValja("1");

let tables = document.body.querySelectorAll("table.LISTA");
let table = tables[3];
let rows = table.getElementsByTagName("tr");
let counter = {
    "totalFixed": 0,
    "totalChecked": 0
}

function checkRow(row) {

    let cells = row.getElementsByTagName("td");
    if (!cells) return;

    if (cells.length > 1) {
        let personnr = cells[1].innerText;
        if (!personnr.match(/^\d{8}-\w{4}$/)) {
            console.log(`Didn't match "${personnr}"`)
            return;
        }
        let checkbox = cells[0].firstChild;

        if (checkbox.checked == true) {
            console.warn("WARNING! A CHECKBOX ALREADY CHECKED!");
            return "fatal";
        }

        counter["totalChecked"]++;
        if (personnrList.includes(personnr)) {
            checkbox.checked = true;
            console.log(`Personnr ${personnr}: Checkbox.checked = ${checkbox.checked}`);
            counter["totalFixed"]++;
        }
    }
}

for (let row of rows) {
    if (checkRow(row) == "fatal") break;
}

console.log(`Checked ${counter['totalFixed']}/${counter['totalChecked']}`);
