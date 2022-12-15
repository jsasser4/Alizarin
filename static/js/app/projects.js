(function () {
    document.getElementById("task-add").onsubmit = (e) => {
        document.getElementById("description").value = document.getElementById("editable-description").innerHTML;
    };
})();

