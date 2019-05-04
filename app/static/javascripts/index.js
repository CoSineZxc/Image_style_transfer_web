function selectImg(file, parm) {
    if (!file.files || !file.files[0]) {
        return;
    }
    let reader = new FileReader();//读取文件
    reader.onload = function (event) {
        if (parm === 1)
            image = document.getElementById("bw_img");
        else if (parm === 2)
            image = document.getElementById("style_img");
        image.src = event.target.result;//读入文件的base64数据(可直接作为src属性来显示图片)
    };
    reader.readAsDataURL(file.files[0]);
}

function selectStyle() {
    let mySelect = document.getElementById("select_style");
    let image = document.getElementById("style_img");
    if (mySelect.options[0].selected !== true) {
        let index = mySelect.selectedIndex;
        // let text = mySelect.options[index].text;
        // if (text=="梵高星空主题")
        // {
        //     dir = "../static/defaultstyle/style1.jpg";
        // }
        dir = "../static/defaultstyle/style" + index.toString() + ".jpg";
        $("#file_upload2").val("");
        image.src = dir;
    } else {
        image.src = "";
    }
}

function uploadImg(parm) {
    let form_data = new FormData();
    let file_info;
    let files1 = $("#file_upload1");
    let files2 = $("#file_upload2");
    let mySelect = document.getElementById("select_style");
    let image = document.getElementById("style_img");

    if (parm === 1) {
        if (files1.val() === "") {
            alert("请上传原始图片");
            return false;
        }
        file_info = files1[0].files[0];
    } else if (parm === 2) {
        if (mySelect.options[0].selected !== true) {
            alert("请先在右侧选择自定义风格");
            return false;
        } else if (files2.val() === "") {
            alert("请上传自定义风格图片");
            return false;
        }
        file_info = files2[0].files[0];
    }

    form_data.append('file', file_info);
    form_data.append('type', parm);
    $.ajax({
        url: "/upload_picture",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
        },
        error: function (returndata) {
            alert(returndata);
        }
    });
}

function trans_pic() {
    if (!$('#bw_img').attr('src')) {
        alert("请上传原始图片");
        return false;
    } else if (!$('#style_img').attr('src')) {
        alert("请选择或上传风格图片");
        return false;
    }
    let filename1;
    let filename2;
    let filepath;
    let form_data = new FormData();

    let mySelect = document.getElementById("select_style");
    let index = mySelect.selectedIndex;
    let text = mySelect.options[index].text;
    if (mySelect.options[0].selected !== true) {
        filename2 = "style"+index.toString() + ".jpg";
        form_data.append("type","default");
    } else {
        filename2 = $("#file_upload2")[0].files[0].name;
        form_data.append("type","customer");
    }

    filename1 = $("#file_upload1")[0].files[0].name;
    form_data.append("filename1", filename1);
    form_data.append("filename2", filename2);
    $.ajax({
        url: "/trans_picture",
        type: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (data) {
            alert("迁移完成");
            console.log(data);
            filename = JSON.parse(data);
            dir = "../static/output/" + filename['filename'];
            //dir="../static/img/"+filename['filename'];
            document.getElementById("fuse_img").src = dir;
        }
    });
}