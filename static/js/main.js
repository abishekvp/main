function load_log(logs){
    const logsTableBody = $(".logsTableBody");
    $(logsTableBody).empty();
    logs.forEach(log => {
        logsTableBody.append(
            `<tr>
                <td>${log.from_number}</td>
                <td>${log.to_number}</td>
                <td>${log.status}</td>
            </tr>`
        );
    });
}

function get_call_log(){
    $.ajax({
        url: `/fetch-call-log`,
        type: "GET",
        success: function (response) {
            load_log(response.logs);
        },
        error: function (error) {
            alert("Error loading log. Error: " + error);
        }
    });
}