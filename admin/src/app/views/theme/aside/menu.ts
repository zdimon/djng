/*
https://keenthemes.com/keen/preview/demo5/components/icons/flaticon.html
*/

export function getMenu(role) {

    const menu = {
        director: [{
            icon: 'flaticon2-map',
            page: '/builder',
            root: true,
            title: 'Media',
            submenu: [
                {
                    title: 'Video',
                    root: true,
                    icon: 'flaticon2-expand',
                    page: '/video',
                },
                {section: 'Components'},
            ],
        },
        {
            title: 'Products',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/products',
        },
        {
            title: 'Log',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/log/list',
        },
        {
            title: 'Customers',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/customers',
        },
        {
            icon: 'flaticon2-browser-2',
            page: '/builder',
            root: true,
            title: 'Director 2',
        },
    ],
        manager: [{
            icon: 'flaticon2-expand',
            page: '/builder',
            root: true,
            title: 'Manager',
        },
        {
            title: 'Products',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/products',
        },
        {
            title: 'Customers',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/customers',
        },
        ],
        admin: [{
            icon: 'flaticon2-map',
            page: '/builder',
            root: true,
            title: 'Media',
            submenu: [
                {
                    title: 'Video',
                    root: true,
                    icon: 'flaticon2-expand',
                    page: '/video',
                },
                {section: 'Components'},
            ],
        },
        {
            title: 'Payments',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/payment',
        },
        {
            title: 'Payment types',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/payment/type',
        },
        {
            title: 'Customers',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/customers',
        },
    ],
        moderator: [{
            icon: 'flaticon2-expand',
            page: '/builder',
            root: true,
            title: 'Moderator',
        },
    
        {
            title: 'Products',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/products',
        },
        {
            title: 'Customers',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/customers',
        },
    ],
        webmaster: [{
            icon: 'flaticon2-expand',
            page: '/builder',
            root: true,
            title: 'Webmaster',
        },
        {
            title: 'Products',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/products',
        },
        {
            title: 'Customers',
            bullet: 'dot',
            icon: 'flaticon-business',
            page: '/ecommerce/customers',
        },
    ],
    };
    return menu[role];

}
