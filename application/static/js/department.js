$(document).ready(function () {

    var table


    function add_department(data) {

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "create_department",
            "method": "POST",
            "headers": {
                "content-type": "application/json",
                "cache-control": "no-cache",
                "postman-token": "2612534b-9ccd-ab7e-1f73-659029967199"
            },
            "processData": false,
            "data": JSON.stringify(data)
        }

        $.ajax(settings).done(function (response) {
            $('.modal.in').modal('hide')
            $.notify("Department Added Successfully", {"status":"success"});
            table.destroy();
            $('#datatable4 tbody').empty(); // empty in case the columns change
            getdepartment()
        });

    }

    function deletedepartment(id) {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "delete/" + id,
            "method": "DELETE_DEPARTMENT",
            "headers": {
                "cache-control": "no-cache",
                "postman-token": "28ea8360-5af0-1d11-e595-485a109760f2"
            }
        }

swal({
    title: "Are you sure?",
    text: "You will not be able to recover this data",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#DD6B55",
    confirmButtonText: "Yes, delete it!",
    closeOnConfirm: false
}, function() {
 $.ajax(settings).done(function (response) {
   swal("Deleted!", "Department has been deleted.", "success");
            table.destroy();
            $('#datatable4 tbody').empty(); // empty in case the columns change
            getdepartment()
        });


});

    }

    function updatedepartment(data, id) {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "edit_department/" + id,
            "method": "EDIT_DEPARTMENT",
            "headers": {
                "content-type": "application/json",
                "cache-control": "no-cache"
            },
            "processData": false,
            "data": JSON.stringify(data)
        }

        $.ajax(settings).done(function (response) {
            $('.modal.in').modal('hide')
            $.notify("Department Updated Successfully", {"status":"success"});
            table.destroy();
            $('#datatable4 tbody').empty(); // empty in case the columns change
            getdepartment()
        });


    }

    function getdepartment() {

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "all_departments",
            "method": "ALL_DEPARTMENTS",
            "headers": {
                "cache-control": "no-cache"
            }
        }

        $.ajax(settings).done(function (response) {



            table = $('#datatable4').DataTable({
                "bDestroy": true,
                'paging': true, // Table pagination
                'ordering': true, // Column ordering
                'info': true, // Bottom left status text
                aaData: response,
                 "aaSorting": [],
                aoColumns: [
                    {
                        mData: 'name'
                    },
                    {
                        mRender: function (o) {
                            return '<button class="btn-xs btn btn-info btn-edit" type="button">Edit</button>';
                        }
                    },
                    {
                        mRender: function (o) {
                            return '<button class="btn-xs btn btn-danger delete-btn" type="button">Delete</button>';
                        }
                    }
        ]
            });
            $('#datatable4 tbody').on('click', '.delete-btn', function () {
                var data = table.row($(this).parents('tr')).data();
                console.log(data)
                deletedepartment(data.id)

            });
            $('.btn-edit').one("click", function(e) {
                var data = table.row($(this).parents('tr')).data();
                $('#content').modal().one('shown.bs.modal', function (e) {
                    for (var key in data) {
                        $("[name=" + key + "]").val(data[key])
                    }
                    $("#savethedepartment").off("click").on("click", function(e) {
                    var instance = $('#department_form').parsley();
                    instance.validate()
                    console.log(instance.isValid())
                    if(instance.isValid()){
                        jsondata = $('#department_form').serializeJSON();
                        updatedepartment(jsondata, data.id)
                        }

                    })
                })



            });

        });


    }


    $("#add_department").click(function () {
$('#department_form input,textarea').val("")
        $('#content').modal().one('shown.bs.modal', function (e) {

console.log('innn')
            $("#savethedepartment").off("click").on("click", function(e) {
            console.log("inn")
            var instance = $('#department_form').parsley();
            instance.validate()
                    if(instance.isValid()){
                jsondata = $('#department_form').serializeJSON();
                add_department(jsondata)
                }

            })

        })



    })


getdepartment()
})