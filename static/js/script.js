/*
 * User: bteam
 * Date: 06.10.11
 * Time: 13:47
 */
dojo.require('dojo.io.iframe');

dojo.require('dijit.form.TextBox');
dojo.require('dijit.form.Button');
dojo.require('dijit.form.Select');
dojo.require('dijit.form.Form');

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.StackContainer");
dojo.require("dijit.layout.ContentPane");

dojo.addOnLoad(function() {
    dojo.query('[type=file]').addClass('dijitTextBox')

    dojo.parser.parse();

    dijit.byId('ajax').onClick = function(e) {
        dojo.stopEvent(e);
        dojo.io.iframe.send({form:'form',handleAs:'json',
            content:{'ajax':true}})
            .then(function(data) {
                console.log(data)
                if (data.img) {
                    var container = new dijit.layout.ContentPane({region:'top'});
                    dojo.create('img',{src:'/static/img/' + data.img},container.domNode);

                    dijit.byId('StackContainer').addChild(container)
                    dijit.byId('StackContainer').selectChild(container)

                    var prev = dojo.create('img',{src:'/static/img/' + data.img,style:'width:80px;margin-bottom:4px;'},dijit.byId('preview').domNode)

                    dojo.connect(prev,'onclick',function(){dijit.byId('StackContainer').selectChild(container)})
                }
            },
            function(e) {
                console.log("error'ульки", e)
            })
    };
});
