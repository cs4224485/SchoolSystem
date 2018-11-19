$(function () {
    desMove();
    inputTitle();
    finishEdit();
    setItemDes();
    addDeleteOption();
    $('.customization').on('click', '.div_table_par', function () {
        $(this).next().last().toggle()
    })
});


function setLineTitle(self) {
    // 设置每行的标题
    var content = self.parent().prev().find('.inputtext').val();
    // 如果content没有内容直接返回
    if (!content){return}
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
        var desItem = $(this).parents('.div_title_attr_question').prev().find('.des,.op-des').eq(thisIndex);
        console.log(desItem.hasClass('op-des'));
        if (desItem.hasClass('op-des')){
            desItem.find('label').text($(this).val())
        }else {
            desItem.text($(this).val())
        }

    })
}

function desMove() {
    // 上下移动选择文字
    $(".customization").on('click', '.design-cup', function () {
        var textValue = $(this).parents('tr').find('.choicetxt').val();
        $(this).parents('tr').find('.choicetxt').attr('value', textValue);
        if ($(this).parents('tr').prevAll().length > 1) {
            var thisIndex = $(this).parents('.tableoption').find('tr').index($(this).parents('tr'));
            // 根据不同类型的表单取值 如 量表还是选择题表
            var tableType = $(this).attr('type');
            if (tableType === 'choice') {
                let desOptions = $(this).parents('.div_title_attr_question').prev().find('.op-des');
                desOptions.eq(thisIndex - 1).before(desOptions.eq(thisIndex));
            } else {
                let desOptions = $(this).parents('.div_title_attr_question').prev().find('.des');
                desOptions.eq(thisIndex - 1).before(desOptions.eq(thisIndex).text(textValue));
            }
            $(this).parents('tr').prev().before($(this).parents('tr').prop('outerHTML'));
            $(this).parents('tr').remove();
        }
    }).on('click', '.design-cdown', function () {
        var textValue = $(this).parents('tr').find('.choicetxt').val();

        $(this).parents('tr').find('.choicetxt').attr('value', textValue);
        if ($(this).parents('tr').nextAll().length > 0) {
            var tableType = $(this).attr('type');
            var thisIndex = $(this).parents('.tableoption').find('tr').index($(this).parents('tr'));
            if (tableType === 'choice') {
                let desOptions = $(this).parents('.div_title_attr_question').prev().find('.op-des');
                desOptions.eq(thisIndex + 1).after(desOptions.eq(thisIndex));
            } else {
                let desOptions = $(this).parents('.div_title_attr_question').prev().find('.des');
                desOptions.eq(thisIndex + 1).after(desOptions.eq(thisIndex).text(textValue));
            }
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

function addDeleteOption() {
            $('.customization').on('click', '.design-add', function () {
                var tbody = $(this).parents('tbody');
                var counter = tbody.find('tr').length;
                var inputHtml = `                                            <tr>
                                                <td style="width: 340px">
                                                    <input type="text" class="choicetxt" tabindex="1"
                                                           style="width: 265px" value="选项${counter}">
                                                    <span title="在此选项下面插入一个新的选项"
                                                          class="choiceimg design-icon design-add"
                                                          style="cursor: pointer; margin-left: 3px;"></span>
                                                    <span title="删除当前选项（最少保留2个选项）"
                                                          class="choiceimg design-icon design-minus"></span>
                                                </td>
                                                <td align="center" style="padding-left: 15px;">
                                                    <span title="将当前选项上移一个位置" class="choiceimg design-icon design-cup"
                                                          style="cursor: pointer;"  type="choice"></span>
                                                    <span title="将当前选项下移一个位置" class="choiceimg design-icon design-cdown"
                                                          style="cursor: pointer;" type="choice"></span>
                                                </td>
                                            </tr>`;

                var optionHtml = `
                                    <li style="width: 99%" class="op-des" >
                                            <a href="###" class="jqRadio" style="position: static"></a>
                                            <label style="vertical-align:middle;padding-left:2px;">选项${counter}</label>
                                    </li>
                `;
                var index = tbody.find('tr').index($(this).parents('tr'));
                $(this).parents('.div_title_attr_question').prev().find('li').eq(index).after(optionHtml);
                $(this).parents('tr').after(inputHtml)
            }).on('click', '.design-minus', function () {
                var tbody = $(this).parents('tbody');
                var counter = tbody.find('tr').length;
                if (counter <= 3) {
                    alert('至少要保留两个选项');
                    return
                }
                var index = tbody.find('tr').index($(this).parents('tr'));
                console.log(index);
                console.log($('.div_table_par').find('li'));
                $('.div_table_par').find('li').eq(index).remove();
                $(this).parents('tr').remove()

            })
        }
