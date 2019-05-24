$(function () {
    desMove();
    inputTitle();
    finishEdit();
    setItemDes();
    $('.customization').on('click', '.div_table_par', function () {
        $(this).next().last().toggle()
    })
});


function setLineTitle(self) {
    // 设置每行的标题
    var content = self.parent().prev().find('.inputtext').val();
    var tableBody = self.parent().parents(".div_title_attr_question").prev().find('tbody');
    tableBody.find('tr').remove();
    content = content.split("\n");
    for (let i = 0; i < content.length; i++) {
        if (content[i] != "") {
            console.log(content[i]);
            var lineTitleHtml = ` <tr>
                                        <th align="left" style="border-bottom: 1px solid #efefef">${content[i]}</th>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>

                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                    </tr>`;
            tableBody.append(lineTitleHtml)
        }
    }
}

function setItemDes() {
    $(".customization").on('blur', '.choicetxt', function () {
        // 设置每个1-5分的描述
        var thisIndex = $(this).parents('.tableoption').find("tr").index($(this).parents('tr'));
        var desItem = $(this).parents('.div_title_attr_question').prev().find('.des').eq(thisIndex);
        desItem.text($(this).val())
    })
}

function desMove() {
    // 上下移动选择文字
    $(".customization").on('click', '.design-cup', function () {
        var textValue = $(this).parents('tr').find('.choicetxt').val();
        $(this).parents('tr').find('.choicetxt').attr('value', textValue);
        if ($(this).parents('tr').prevAll().length > 1) {
            var desOptions = $(this).parents('.div_title_attr_question').prev().find('.des');
            var thisIndex = $(this).parents('.tableoption').find('tr').index($(this).parents('tr'));
            desOptions.eq(thisIndex - 1).before(desOptions.eq(thisIndex).text(textValue));
            $(this).parents('tr').prev().before($(this).parents('tr').prop('outerHTML'));
            $(this).parents('tr').remove();

        }
    }).on('click', '.design-cdown', function () {
        var textValue = $(this).parents('tr').find('.choicetxt').val();
        $(this).parents('tr').find('.choicetxt').attr('value', textValue);
        if ($(this).parents('tr').nextAll().length > 0) {
            var desOptions = $(this).parents('.div_title_attr_question').prev().find('.des');
            var thisIndex = $(this).parents('.tableoption').find('tr').index($(this).parents('tr'));
            desOptions.eq(thisIndex + 1).after(desOptions.eq(thisIndex).text(textValue));
            $(this).parents('tr').next().after($(this).parents('tr').prop('outerHTML'));
            $(this).parents('tr').remove()
        }
    })
}

function inputTitle() {
    $(".customization").on('input', '.scale-title', function () {
        $(this).parents('.div_question').find("h3").text($(this).val())
    })
}

function finishEdit() {
    $('.customization').on('click', '.submitbutton', function () {
        setLineTitle($(this));
        $(this).parents('.div_title_attr_question').css('display', 'none')
    })
}