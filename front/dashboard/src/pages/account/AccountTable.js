// src/pages/account/AccountTable.js

import PropTypes from 'prop-types';
import React, { useEffect, useState, forwardRef } from 'react';

// MUI v5 Components
import { Box, Skeleton, Typography, Stack, TableHead, TableFooter, TableRow, TableCell } from '@mui/material';

// Material Table Core
import MaterialTable, { MTableBody } from '@material-table/core';

// MUI v5 Icons
import AddBox from '@mui/icons-material/AddBox';
import ArrowDownward from '@mui/icons-material/ArrowDownward';
import Check from '@mui/icons-material/Check';
import ChevronLeft from '@mui/icons-material/ChevronLeft';
import ChevronRight from '@mui/icons-material/ChevronRight';
import Clear from '@mui/icons-material/Clear';
import DeleteOutline from '@mui/icons-material/DeleteOutline';
import Edit from '@mui/icons-material/Edit';
import FilterList from '@mui/icons-material/FilterList';
import FirstPage from '@mui/icons-material/FirstPage';
import LastPage from '@mui/icons-material/LastPage';
import Remove from '@mui/icons-material/Remove';
import SaveAlt from '@mui/icons-material/SaveAlt';
import Search from '@mui/icons-material/Search';
import ViewColumn from '@mui/icons-material/ViewColumn';

// Third-party
import NumberFormat from 'react-number-format';

// Project imports
import Dot from 'components/@extended/Dot';
import axios from 'axios';
import Moment from 'moment';
import { useRecoilValue } from 'recoil';
import { authAtom } from '_state';

// Define table icons
const tableIcons = {
    Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
    Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
    Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
    DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
    Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
    Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
    FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
    LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
    NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
    ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
    SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
    ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
    ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />)
};

// Table Head Component
function descendingComparator(a, b, transactionBy) {
    if (b[transactionBy] < a[transactionBy]) {
        return -1;
    }
    if (b[transactionBy] > a[transactionBy]) {
        return 1;
    }
    return 0;
}

function getComparator(transaction, transactionBy) {
    return transaction === 'desc'
        ? (a, b) => descendingComparator(a, b, transactionBy)
        : (a, b) => -descendingComparator(a, b, transactionBy);
}

function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
        const transaction = comparator(a[0], b[0]);
        if (transaction !== 0) {
            return transaction;
        }
        return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
}

const headCells = [
    {
        id: 'date',
        align: 'left',
        disablePadding: true,
        label: 'Date'
    },
    {
        id: 'name',
        align: 'left',
        disablePadding: true,
        label: 'Transaction Name'
    },
    {
        id: 'fat',
        align: 'left',
        disablePadding: false,
        label: 'Category'
    },
    {
        id: 'protein',
        align: 'right',
        disablePadding: false,
        label: 'Amount'
    }
];

function TransactionTableHead({ transaction, transactionBy }) {
    return (
        <TableHead>
            <TableRow>
                {headCells.map((headCell) => (
                    <TableCell
                        key={headCell.id}
                        align={headCell.align}
                        padding={headCell.disablePadding ? 'none' : 'normal'}
                        sortDirection={transactionBy === headCell.id ? transaction : false}
                    >
                        {headCell.label}
                    </TableCell>
                ))}
            </TableRow>
        </TableHead>
    );
}

TransactionTableHead.propTypes = {
    transaction: PropTypes.string,
    transactionBy: PropTypes.string
};

// Transaction Status Component
const TransactionStatus = ({ status }) => {
    let color;
    let title;

    switch (status) {
        case 0:
            color = 'warning';
            title = 'Pending';
            break;
        case 1:
            color = 'success';
            title = 'Approved';
            break;
        case 2:
            color = 'error';
            title = 'Rejected';
            break;
        default:
            color = 'primary';
            title = 'None';
    }

    return (
        <Stack direction="row" spacing={1} alignItems="center">
            <Dot color={color} />
            <Typography>{title}</Typography>
        </Stack>
    );
};

TransactionStatus.propTypes = {
    status: PropTypes.number
};

// Main AccountTable Component
export default function AccountTable(props) {
    const [transaction, setTransaction] = useState('asc');
    const [transactionBy, setTransactionBy] = useState('trackingNo');
    const [selected] = useState([]);
    const [data, setData] = useState([{}]);
    const [accounts, setAccounts] = useState();
    const [total, setTotal] = useState(null);
    const token = useRecoilValue(authAtom);
    const [showloader, setshowloader] = useState(true);

    const API_URL = process.env.REACT_APP_API_URL;
    const Authorization = 'Token ' + token;
    const isSelected = (trackingNo) => selected.indexOf(trackingNo) !== -1;

    const loadAccounts = async () => {
        try {
            let url = `${API_URL}/user_accounts/`;
            let response = await axios.get(url, {
                headers: { Authorization: Authorization }
            });
            if (response.status === 200) {
                setData(response.data);
                let sum = response.data.map((item) => item.balance).reduce((prev, next) => prev + next, 0);
                setTotal(sum);
                return true;
            }
        } catch (error) {
            console.error(error);
            return false;
        }
    };

    useEffect(() => {
        loadAccounts().then((success) => {
            if (success) {
                setshowloader(false);
            }
        });
    }, []);

    return (
        <Box>
            {showloader === false ? (
                <MaterialTable
                    icons={tableIcons}
                    data={data}
                    options={{
                        search: false,
                        selection: false,
                        showTitle: false,
                        toolbar: false,
                        grouping: true,
                        defaultExpanded: true,
                        paging: false
                    }}
                    columns={[
                        { title: 'Account Name', field: 'company', editable: 'never' },
                        { title: 'Type', field: 'type', editable: 'never', defaultGroupOrder: 0 },
                        { title: 'Balance', field: 'balance', type: 'numeric', editable: 'never' }
                    ]}
                    components={{
                        Body: (props) => (
                            <>
                                <MTableBody {...props} />
                                <TableFooter>
                                    <TableRow>
                                        <TableCell colSpan={2}>Total:</TableCell>
                                        <TableCell colSpan={2} align={'right'}>
                                            {total}
                                        </TableCell>
                                    </TableRow>
                                </TableFooter>
                            </>
                        )
                    }}
                    cellEditable={{
                        onCellEditApproved: (newValue, oldValue, rowData, columnDef) => {
                            return new Promise(async (resolve, reject) => {
                                // Implement your cell edit logic here
                                // For now, it's just resolving after a delay
                                setTimeout(resolve, 1000);
                            });
                        }
                    }}
                />
            ) : (
                <Box sx={{ pt: 0.5, width: '100%', height: '100%' }}>
                    <Skeleton animation="wave" variant="rectangular" height={220} />
                    <Skeleton animation="wave" />
                    <Skeleton animation="wave" />
                    <Skeleton animation="wave" />
                    <Skeleton animation="wave" width="60%" />
                    <Skeleton animation="wave" width="60%" />
                    <Skeleton animation="wave" width="60%" />
                </Box>
            )}
        </Box>
    );
}

AccountTable.propTypes = {
    // Define your prop types if needed
};

