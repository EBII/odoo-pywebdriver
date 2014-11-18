openerp.base_pywebdriver = function(instance) {

instance.base_pywebdriver.ConfirmWidget = instance.web.Widget.extend({
    start: function() {
        var self = this;
        this.$el.append("<div>Click on the button for search connected pywebdriver on network.</div>" +
            "<button class='search_button'>Search</button>");
        this.$el.find("button.search_button").click(function() {
            self.trigger("find_proxy", true);
        });

    },
});

instance.base_pywebdriver.Discovery = instance.web.Widget.extend({

    list_action_id: 'base_pywebdriver.pywebdriver_server_tree_action',

    start: function() {
        var widget = new instance.base_pywebdriver.ConfirmWidget(this);
        widget.on("find_proxy", this, this.find_proxy);
        widget.appendTo(this.$el);
    },

    find_proxy: function(){
            options = {};
            var self  = this;
            var port  = ':' + (options.port || '8069');
            var urls  = [];
            var found = false;
            var parallel = 8;
            var done = new $.Deferred(); // will be resolved with the proxies valid urls
            var threads  = [];
            var progress = 0;
            var url_server = '';

        urls.push('http://localhost'+port);
        for(var i = 0; i < 256; i++){
            urls.push('http://192.168.0.'+i+port);
            urls.push('http://192.168.1.'+i+port);
            urls.push('http://10.0.0.'+i+port);
        }

            var prog_inc = 1/urls.length;

            function update_progress(){
                progress = found ? 1 : progress + prog_inc;
                if(options.progress){
                    options.progress(progress);
                }
            }

            function thread(done){
                var url = urls.shift();

                done = done || new $.Deferred();

                if( !url || found || !self.searching_for_proxy ){
                    done.resolve();
                    return done;
                }

                var c = $.ajax({
                        url: url + '/hw_proxy/hello',
                        method: 'GET',
                        timeout: 400,
                    }).done(function(){
                        found = true;
                        update_progress();
                        done.resolve(url);
                    })
                    .fail(function(){
                        update_progress();
                        thread(done);
                    });

                return done;
            }

            this.searching_for_proxy = true;

            for(var i = 0, len = Math.min(parallel,urls.length); i < len; i++){
                threads.push(thread());
            }

            $.when.apply($,threads).then(function(){

                new instance.web.Model("pywebdriver.server").call("update_state_server", [arguments]);

                for(var i = 0; i < arguments.length; i++){
                    if(arguments[i]){
                        url_server = arguments[i];
                        var c = $.ajax({
                                url: arguments[i] + '/cups/getPrinters',
                                method: 'GET',
                                timeout: 400,
                            }).done(function(data){
                                new instance.web.Model("pywebdriver.server").call("update_list_server", [url_server, data.result]);
                        })
                }
            }
                done.resolve();
            });
            return done;
        },
    }
);

instance.web.client_actions.add("discovery", "instance.base_pywebdriver.Discovery");

};
