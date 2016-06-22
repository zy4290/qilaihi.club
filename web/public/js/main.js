/**
 * Created by huhai on 2016/6/12.
 */
$(function(){
    /*success*/
    $('.share a').click(function(){
        $('.share').hide();
    });
    /*弹框*/
    $('.weui_btn_dialog').click(function(){
        $(this).parents('.weui_dialog_alert').hide();
    })
});