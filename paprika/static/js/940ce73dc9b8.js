$(document).ready(function(){$("#add_flow_btn").click(function(){$("#dialogs").fadeIn(200,function(){$("#add_flow_dialog").fadeIn(200);});});$(".close_dialog, .close").click(function(){$(this).parent().fadeOut(200,function(){$("#dialogs").fadeOut(200);});});$("#add_stage_btn").click(function(){var container=$("#stage_form_list");var stage_form=$("<div class='stage_form'></div>");stage_form.append("<input type='text' class='title' name='stage_titles' placeholder='Stage title' />");stage_form.append("<input type='text' class='description' name='stage_descriptions' placeholder='Stage description' />");stage_form.append("<div class='btn btn_red remove_stage'>x</div>");container.append(stage_form);});$(".remove_stage").live('click',function(){var stage_form=$(this).parent();stage_form.remove();});$(".delete_btn").click(function(){currentFlow=$(this).parent().parent();$("#dialogs").fadeIn(200,function(){$("#delete_flow_dialog").fadeIn(200);});});$("#yes_delete_btn").click(function(){flowId=$(currentFlow).attr("data-flowid");$.ajax({beforeSend:function(xhr,settings){xhr.setRequestHeader("X-CSRFToken",$.cookie('csrftoken'));},type:"POST",url:"/ajax/delete_flow/",data:{"flow_id":flowId},async:true,success:function(response){console.log(response);},error:function(response){console.log(response);}});$("#delete_flow_dialog").fadeOut(200,function(){$("#dialogs").fadeOut(200);});$(currentFlow).delay(400).slideUp(200);});});