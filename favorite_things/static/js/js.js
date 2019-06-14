var active = "";
var active_name = "";
function submit(){
    $("#submit-bt").html('<div class="lds-spinner"><div></div><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
    var title = $("#title").val();
    var description = $("#description").val();
    var category = $("#category").val();
    var ranking = $("#ranking").val();
    if(title !== ""){
                if(category !== ""){
                        if(ranking > 0){
                            $.post('/add', {title:title, description:description, category:category,
                                ranking:ranking, user_id:active},function (data) {
                                $("#submit-bt").html('SUBMIT');
                                if(data['message'] === "Request was successfully added to your favorite list."){
                                    Lobibox.notify('success', {
                                        showClass: 'fadeIn',
                                        hideClass: 'fadeOut',
                                        msg: data['message']
                                    });
                                    $("#title").val('');
                                    $("#description").val('');
                                    $("#category").val('');
                                    $("#ranking").val("")
                                }else{
                                    Lobibox.notify('error', {
                                        showClass: 'fadeIn',
                                        hideClass: 'fadeOut',
                                        msg: data['message']
                                    });
                                }
                            });
                        }else{
                            $("#submit-bt").html('SUBMIT');
                            Lobibox.notify('error', {
                                showClass: 'fadeIn',
                                hideClass: 'fadeOut',
                                msg: "The ranking must be greater than zero."
                            });
                        }
                }else{
                    $("#submit-bt").html('SUBMIT');
                    Lobibox.notify('error', {
                        showClass: 'fadeIn',
                        hideClass: 'fadeOut',
                        msg: "Category is required."
                    });
                }
    }else{
        $("#submit-bt").html('SUBMIT');
      Lobibox.notify('error', {
                    showClass: 'fadeIn',
                    hideClass: 'fadeOut',
                    msg: "The Title field is required!"
                });
    }

}

function nav(a) {
    $(".navz").removeClass('active');
    $("#"+a+"-bt").addClass('active');
    $("#content").html('<center style="margin-top: 20%;"><div class="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></center>');
    if(a === "list") {
        $.post('/list', {user: active}, function (data) {
            $("#content").html(data);
        });
    }else if(a === "home"){
        $.post('/home', {user: active}, function (data) {
            $("#content").html(data);
        });
    }
}
var t = "";
var d = "";
var c = "";
var r = "";

function edit_list(a, b) {
    var title = $("#"+a+String(b)+"title");
    title.removeAttr('readonly');
    title.focus();
    var des = $("#"+a+String(b)+"description");
    des.removeAttr('readonly');
    var cat = $("#"+a+String(b)+"category");
    cat.removeAttr('disabled');
    var rank = $("#"+a+String(b)+"ranking");
    rank.removeAttr('readonly');
    var edit_bt = $("#"+a+String(b)+"edit-bt");
    edit_bt.html('<i class="glyphicon glyphicon-ok"></i> SAVE');
    edit_bt.attr('onclick', 'save_list(\''+a+'\', \''+b+'\')');
    t = title.val();
    d = des.val();
    c = cat.val();
    r = rank.val();

}

function save_list(a, b) {
    var edit_bt = $("#"+a+String(b)+"edit-bt");
    edit_bt.html('<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div>' +
        '<div></div><div></div><div></div><div></div><div></div><div></div></div>');
    var title = $("#"+a+String(b)+"title");
    var des = $("#"+a+String(b)+"description");
    var cat = $("#"+a+String(b)+"category");
    var rank = $("#"+a+String(b)+"ranking");
    var tt = title.val();
    var dd = des.val();
    var cc = cat.val();
    var rr = rank.val();
    if(title.val() !== ""){
        var move = Boolean(1);
        if(des.val() !== ""){
            var len = des.val().length;
            if(len >= 10){

            }else{
                move = Boolean(0);
            }
        }
        if(move === Boolean(1)){
            if(cat.val() !== ""){
                if(rank.val() > 0){
                    $.post('/edit', {id:b, title:title.val(), description:des.val(), cat:cat.val(),
                        ranking:rank.val(), user_id: active}, function(data){
                       if(data === "<Response [204]>"){
                           title.attr('readonly', 'readonly');
                           des.attr('readonly', 'readonly');
                           cat.attr('disabled', 'disabled');
                           rank.attr('readonly', 'readonly');
                           edit_bt.html('<i class="glyphicon glyphicon-pencil"></i> EDIT');
                           edit_bt.attr('onclick', 'edit_list(\''+a+'\', \''+b+'\')');
                           if(t !== tt || d !== dd || c !== cc || r !== rr){
                               var dt = new Date();
                               var ddt = dt.getFullYear()+"-"+dt.getMonth()+"-"+dt.getDay();
                               $("#"+a+String(b)+"last-mod").html(ddt);
                               Lobibox.notify('success', {
                                showClass: 'fadeIn',
                                hideClass: 'fadeOut',
                                msg: "This favorite list was successfully updated."
                            });
                           }

                       }else{
                           edit_bt.html('<i class="glyphicon glyphicon-pencil"></i> EDIT');
                           edit_bt.attr('onclick', 'edit_list(\''+a+'\', \''+b+'\')');
                           Lobibox.notify('error', {
                                showClass: 'fadeIn',
                                hideClass: 'fadeOut',
                                msg: "Oops! An error occur while trying to update list."
                            });
                       }
                    });
                }else{
                    Lobibox.notify('error', {
                        showClass: 'fadeIn',
                        hideClass: 'fadeOut',
                        msg: "Oops! The ranking value must be greater than zero."
                    });
                }
            }else{
                Lobibox.notify('error', {
                    showClass: 'fadeIn',
                    hideClass: 'fadeOut',
                    msg: "Oops! You have to select a category."
                });
            }

        }else{
          Lobibox.notify('error', {
            showClass: 'fadeIn',
            hideClass: 'fadeOut',
            msg: "Oops! The description field must be greater or equal to 10 characters if not empty."
        });
        }
    }else{
        Lobibox.notify('error', {
            showClass: 'fadeIn',
            hideClass: 'fadeOut',
            msg: "Oops! The title field is required."
        });
    }

}

function log_list(a, b) {
    $("#modal").modal("show");
    $.post('/log', {id:b}, function (data) {
       $("#put-stuffs").html(data);
    });
}

function new_cat(){
    var bt = $("#new-cat-bt");
    bt.html('<div class="lds-spinner"><div></div><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
    var cat = $("#new-cat");
    if(cat.val() !== ""){
        $.post('/cat/new', {user_id: active, name: cat.val()}, function(data) {
            bt.html('<i class="glyphicon glyphicon-plus"></i> Add');
            if (data === "success") {
            cat.val('');
            Lobibox.notify('success', {
           showClass: 'fadeIn',
           hideClass: 'fadeOut',
           msg: "New category successfully added."
       });
        }else{
                bt.html('<i class="glyphicon glyphicon-plus"></i> Add');
               Lobibox.notify('error', {
                   showClass: 'fadeIn',
                   hideClass: 'fadeOut',
                   msg: "Oops! An error occur while attempting to add new category"
                });
        }
        });
    }else{
        bt.html('<i class="glyphicon glyphicon-plus"></i> Add');
        Lobibox.notify('error', {
           showClass: 'fadeIn',
           hideClass: 'fadeOut',
           msg: "Oops! You can't submit an empty field!"
        });
    }
}


function sort() {
    var cat = $("#sort").val();
    var contain = $("#list-cont");
    contain.html('<center style="margin-top: 20%;"><div class="lds-roller"><div></div><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div></div></center>');
    if(cat === "") {
        $.post('/sort', {user: active, cat:""}, function (data) {
            contain.html(data);
        });
    }else{
        $.post('/sort', {user: active, cat:cat}, function (data) {
            contain.html(data);
        });
    }
}

function login_form(){
    if(active === "" && active_name === "") {
        $("#content").html('<center style="margin-top: 20%;"><div class="lds-roller"><div></div><div></div><div>' +
            '</div><div></div><div></div><div></div><div></div><div></div></div></center>');
        $.get('/signin', {}, function (data) {
            $("#content").html(data);
        });
    }else{
        nav('home');
    }
}

function reg_form(){
    $("#content").html('<center style="margin-top: 20%;"><div class="lds-roller"><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div><div></div></div></center>');
    $.get('/signup', {}, function(data){
        $("#content").html(data);
    });
}

function submit_reg(){
    $("#reg-bt").html('<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
    var username = $("#reg-username");
    var email = $("#reg-email");
    var pass = $("#reg-pass");
    var conf = $("#reg-pass-conf");
    if(username.val() !== ""){
        if(email.val() !== ""){
            if(pass.val() === conf.val()){
                $.post('/register', {username:username.val(), email:email.val(), password:pass.val()}, function(data){
                  $("#reg-bt").html('SUBMIT');
                  data = data.split("//");
                  if(data[0] === "success"){
                      username.val('');
                      email.val('');
                      pass.val('');
                      conf.val('');
                      Lobibox.notify('success', {
                          showClass: 'fadeIn',
                          hideClass: 'fadeOut',
                          msg: "Successfully signed up."
                      });
                      login_form();
                  }else if(data[0] === "error"){
                      Lobibox.notify('error', {
                          showClass: 'fadeIn',
                          hideClass: 'fadeOut',
                          msg: data['message']
                      });
                  }

                });
            }else{
                $("#reg-bt").html('SUBMIT');
                Lobibox.notify('error', {
                    showClass: 'fadeIn',
                    hideClass: 'fadeOut',
                    msg: "Oops! Passwords do not match."
                });
            }
        }else{
            $("#reg-bt").html('SUBMIT');
            Lobibox.notify('error', {
                showClass: 'fadeIn',
                hideClass: 'fadeOut',
                msg: "Oops! The email field is required."
            });
        }
    }else{
        $("#reg-bt").html('SUBMIT');
        Lobibox.notify('error', {
            showClass: 'fadeIn',
            hideClass: 'fadeOut',
            msg: "Oops! A username is required."
        });
    }
}


function login(){
    $("#login-bt").html('<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
    var user = $("#login-user");
    var pass = $("#login-pass");
    if(user.val() !== ""){
        if(pass.val() !== ""){
            $.post('/login', {email:user.val(), password:pass.val()}, function(data){
              $("#login-bt").html('LOGIN');
              var cred = data.split("//");
              if(cred[0] === "success"){
                  user.val('');
                  pass.val('');
                  active = cred[1];
                  active_name = cred[2];
                  nav('home');
                  $("#list-bt").removeClass('hidden');
                  $("#active").removeClass('hidden');
                  $("#logout").removeClass('hidden');
                  $("#active-name").html(active_name);
              }else if(cred[0] === "error"){
                  Lobibox.notify('error', {
                      showClass: 'fadeIn',
                      hideClass: 'fadeOut',
                      msg: cred[1]
                  });
              }

            });

        }else{
            $("#login-bt").html('LOGIN');
            Lobibox.notify('error', {
                showClass: 'fadeIn',
                hideClass: 'fadeOut',
                msg: "Oops! The password field is required."
            });
        }
    }else{
        $("#login-bt").html('LOGIN');
        Lobibox.notify('error', {
            showClass: 'fadeIn',
            hideClass: 'fadeOut',
            msg: "Oops! A email field is required."
        });
    }
}

function logout(){
    window.document.location.assign(String(document.location).split("#")[0]);
}