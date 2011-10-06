/*
 * User: bteam
 * Date: 06.10.11
 * Time: 13:47
 */
dojo.require('dojo.io.iframe');

dojo.require('dijit.form.TextBox');
dojo.require('dijit.form.Button');
dojo.require('dijit.form.Select');

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");

dojo.addOnLoad(function() {

    dojo.query('[type=file]').addClass('dijitTextBox')

    dojo.parser.parse();
    var select = new dijit.form.Select(null,'id_font');
    dijit.byId('ajax').onClick = function(e) {
        dojo.stopEvent(e);
        dojo.io.iframe.send({form:'form',handleAs:'json',
            content:{'ajax':true}})
            .then(function(data) {
                console.log(data)
                if (data.img) {
                    setTimeout(function() {
                        dojo.create('img', {src:'/static/img/' + data.img,
                            height:dijit.byId('content').h}, 'olo');
                    }, 1000)

                }
            },
            function(e) {
                console.log("error'ульки", e)
            })
    };
});