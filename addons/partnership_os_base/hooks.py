MENUS_TO_HIDE = [
    'stock.menu_stock_root',
    'mrp.menu_mrp_root',
    'point_of_sale.menu_point_root',
    'website.menu_website_configuration',
    'purchase.menu_purchase_root',
    'mass_mailing.mass_mailing_menu_root',
    'event.event_main_menu',
    'survey.menu_surveys',
    'maintenance.menu_maintenance_requests',
    'fleet.fleet_menu_root',
    'lunch.lunch_menu_root',
    'sale_management.sale_menus_root',
]


def post_init_hook(env):
    for ref in MENUS_TO_HIDE:
        menu = env.ref(ref, raise_if_not_found=False)
        if menu:
            menu.write({'active': False})
