/*
SPDX-License-Identifier: LGPL-2.1-or-later


SPDX-FileCopyrightText: 2023 The TracTicketMSTeamsDispatcherPlugin Authors
*/

/*
 this is just ugly, but it does the job we pass a list of json dicts into the function to
 convert them into js objects to we can iterate over them and access the values.

 THIS IS NOT THE WAY IT SHOULD BE BUT THE LACK OF KNOWING HOW TO DO IT DIFFRENTLY RESULTS IN
 CODE LIKE THIS ...

 and no i don't do frontend ...
*/

function add_web_hook(presets) {
  var whc = $("#web_hook_container")
  var counter = whc.children("div.ttmsd-fieldset").length + 1;
  let fs = $(`<div class=\"ttmsd-fieldset\">`).append(`<div class=\"ttmsd-py-1 ttmsd-fieldset-legend ttmsd-bg-heading\">Settings</div> `)
  fs.appendTo(whc)
  let iname = $(`<div class=\"ttmsd-input-group ttmsd-p-1\"> \
  <label class=\"ttmsd-input-group-text\">Connector Name:</label> \
  <input type=\"text\" class=\"ttmsd-b-1\" id=\"web_hook_name_${counter}\" name=\"web_hook_name_${counter}\" value=\"\" size=\"48\"/> \
  </div>`)
  iname.appendTo(fs)
  let iurl = $(`<div class=\"ttmsd-input-group ttmsd-p-1\"> \
  <label class=\"ttmsd-input-group-text\">Connector URL:</label> \
  <input type=\"text\" class=\"ttmsd-b-1\" id=\"web_hook_url_${counter}\" name=\"web_hook_url_${counter}\" value=\"\" size=\"48\"/> \
  </div>`)
  iurl.appendTo(fs)
  let igt = $(`<div class=\"ttmsd-input-group ttmsd-p-1\" />`).append(`<label class=\"ttmsd-input-group-text\">Connector Typ:</label>`)
  igt.appendTo(fs)
  let s = $(`<select name=\"web_hook_type_${counter}\" ></select>`).appendTo(igt);
  presets.forEach(preset => {
    let p = JSON.parse(preset);
    $("<option />", { value: p.id, text: p.name }).appendTo(s);
  })
  let ihd = $(`<input type=\"hidden\" name=\"action-${counter}\" value=\"delete-${counter}\" />`)
  ihd.appendTo(fs)
  let dbtn = $(`<Button type=\"button\" class=\"ttmsd-btn\" id=\"delete-button-${counter}\" onclick=\"remove_web_hook(this.id)\">delete</button>`)
  dbtn.appendTo(fs)
}

function remove_web_hook(val, del_input, webhook_id) {
  jQuery(document).ready(function ($) {
    let dil = $(`#${del_input}`)
    let btn = $(`#${val}`)

    let dil_val = dil.val() + "," + webhook_id
    dil.val(dil_val)
    let fs = btn.closest("div.ttmsd-fieldset")
    fs.remove()

    console.debug(dil.val)
  });
}
function add_fact(ele, presets, change) {
  let parts = ele.id.split("_")
  let payload_id = parts[1]
  let section_id = parts[parts.length - 1]
  let whc = $(ele)
  //let counter = whc.children("div.ttmsd-flex-row").length + 1;
  let counter = `n${payload_id}${section_id}${(whc.children("div.ttmsd-flex-row").length + 1) * 10}`
  let fs = $(`<div class=\"ttmsd-flex-row\" />`).append($(`<div class=\"ttmsd-input-group ttmsd-p-1\"> \
  <label class=\"ttmsd-input-group-text\" for="teams_${payload_id}_fact_name_${section_id}_${counter}\">Name:</label>
  <input class=\"ttmsd-b-1\" type=\"text\" id=\"teams_${payload_id}_fact_name_${section_id}_${counter}\"
  name=\"teams_${payload_id}_fact_name_${section_id}_${counter}\" value=\"\" size=\"50\" /> \
  </div>`));
  let div_value = $(`<div class=\"ttmsd-input-group ttmsd-p-1\" />`).appendTo(fs);
  div_value.append($(`<label class="ttmsd-input-group-text" for=\"teams_${payload_id}_fact_value_${section_id}_${counter}">Value:</label>`));
  let s = $(`<select name=\"teams_${payload_id}_fact_value_${section_id}_${counter}\" ></select>`);
  s.appendTo(div_value)

  $(`<Button type=\"button\" class=\"ttmsd-btn\" id=\"teams_${payload_id}_fact_delete_${section_id}_${counter}\" \
  onclick="remove_fact(this.id)">delete'</Button></div>`).appendTo(fs);
  whc.append(fs);
}

function remove_fact(val) {
  jQuery(document).ready(function ($) {
    var fs = $(`#${val}`).closest("div.ttmsd-flex-row")
    fs.remove()
  });
}
