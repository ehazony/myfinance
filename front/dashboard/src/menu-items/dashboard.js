// assets
import { DashboardOutlined } from '@ant-design/icons';

// icons
const icons = {
    DashboardOutlined
};

// ==============================|| MENU ITEMS - DASHBOARD ||============================== //

const dashboard = {
    id: 'group-dashboard',
    title: 'Navigation',
    type: 'group',
    children: [
        {
            id: 'dashboard',
            title: 'Dashboard',
            type: 'item',
            url: '/dashboard/default',
            icon: icons.DashboardOutlined,
            breadcrumbs: false
        },
        {
            id: 'dashboard-transactions',
            title: 'Transactions',
            type: 'item',
            url: '/dashboard/transactions',
            icon: icons.DashboardOutlined,
            breadcrumbs: false
        },
        {
            id: 'dashboard-accounts',
            title: 'Accounts',
            type: 'item',
            url: '/dashboard/accounts',
            icon: icons.DashboardOutlined,
            breadcrumbs: false
        }
    ]
};

export default dashboard;
