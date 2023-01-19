/*
  SPDX-License-Identifier: LGPL-2.1-or-later


  SPDX-FileCopyrightText: 2023 The TracTicketMSTeamsDispatcherPlugin Authors
*/

function add_web_hook(){
  var whc = $("#web_hook_container")
  var counter = whc.children("fieldset").length + 1;
  whc.append(
    `<fieldset> \
    <legend>Settings</legend> \
    <div class=\"field\"> \
    <label>Connector Name:<br /> \
    <input type=\"text\" id=\"web_hook_name_${counter}\" name=\"web_hook_name_${counter}\" value=\"\" size=\"48\"/> \
    </label> \
    <div class=\"field\"> \
    <label>Connector URL:<br /> \
            <input type=\"text\" id=\"web_hook_url_${counter}\" name=\"web_hook_url_${counter}\" value=\"\" size=\"48\"/> \
            </label> \
      <div class=\"field\"> \
      <label>Connector Typ:<br /> \
      <select name=\"web_hook_type_${counter}\"> \
      <option value=\"MS Teams\" SELECTED>MS Teams</option> \
            <option value=\"Discord\" >Discord</option> \
        </select> \
        </label> \
        <div class=\"buttons\"> \
        <input type=\"hidden\" name=\"action-${counter}\" value=\"delete-${counter}\" /> \
        <Button type=\"button\" id=\"delete-button-${counter}\" onclick=\"remove_web_hook(this.id)\">delete</button>\
        </div> \
        </div> \
        </fieldset>`
)}

function remove_web_hook(val)
{
  jQuery(document).ready(function($) {
    var whc = $("#web_hook_container")
    var fs = $(`#${val}`).closest("fieldset")
    fs.remove()

  });
}
