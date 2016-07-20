var chat_html = new DESK.Widget({
    version: 1,
    id: 'support-chat',
    site: 'buzzhire.desk.com',
    port: '80',
    type: 'chat',
    displayMode: 1,  //0 for popup, 1 for lightbox
    features: {
            offerAlways: true,
            offerAgentsOnline: false,
            offerRoutingAgentsAvailable: false,
            offerEmailIfChatUnavailable: false
    },
    fields: {
            ticket: {
                // desc: &#x27;&#x27;,
                // labels_new: &#x27;&#x27;,
                // priority: &#x27;&#x27;,
                // subject: &#x27;&#x27;
            },
            interaction: {
                // email: &#x27;&#x27;,
                // name: &#x27;&#x27;
            },
            chat: {
                //subject: ''
            },
            customer: {
                // company: &#x27;&#x27;,
                // desc: &#x27;&#x27;,
                // first_name: &#x27;&#x27;,
                // last_name: &#x27;&#x27;,
                // locale_code: &#x27;&#x27;,
                // title: &#x27;&#x27;,
                // custom_category: &#x27;&#x27;,
                // custom_appointment: &#x27;&#x27;,
                // custom_appointment_confirmation: &#x27;&#x27;
            }
    }
}).render();