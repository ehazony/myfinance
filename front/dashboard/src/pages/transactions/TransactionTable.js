import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';

import { forwardRef } from 'react';

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
import Dot from 'components/@extended/Dot';
import axios from 'axios';
import Moment from 'moment';
import { useRecoilValue } from 'recoil';
import { authAtom } from '_state';
import MaterialTable from '@material-table/core';
// material-ui
import { Box, Link, Skeleton, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

// third-party
import NumberFormat from 'react-number-format';


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

// project import

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

// ==============================|| Transaction TABLE - HEADER CELL ||============================== //

const headCells = [
    // {
    //     id: 'trackingNo',
    //     align: 'left',
    //     disablePadding: false,
    //     label: 'Tracking No.'
    // },
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
    // {
    //     id: 'carbs',
    //     align: 'left',
    //     disablePadding: false,
    //
    //     label: 'Category'
    // },
    {
        id: 'protein',
        align: 'right',
        disablePadding: false,
        label: 'Amount'
    }
];

// ==============================|| Transaction TABLE - HEADER ||============================== //

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

// ==============================|| Transaction TABLE - STATUS ||============================== //

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

// ==============================|| Transaction TABLE ||============================== //

export default function TransactionTable(props) {
    const [Transaction] = useState('asc');
    const [transactionBy] = useState('trackingNo');
    const [selected] = useState([]);
    const [data, setData] = useState([{}]);
    const [categories, setCategories] = useState();
    const token = useRecoilValue(authAtom);
    const [showloader, setshowloader] = useState('true');

    const API_URL = process.env.REACT_APP_API_URL;
    const Authorization = 'Token ' + token;
    const isSelected = (trackingNo) => selected.indexOf(trackingNo) !== -1;
    function startOfMonth(date) {
        return new Date(date.getFullYear(), date.getMonth(), 1);
    }
    function endOfMonth(date) {
        return new Date(date.getFullYear(), date.getMonth() + 1, 0);
    }
    const setDataFromEndpoint = async () => {
        try {
            let date = props.date;
            if (date === undefined) {
                date = new Date();
            }
            const start = startOfMonth(date).toString();
            const end = endOfMonth(date).toString();
            const dateParam = '?date__gte=' + Moment(start).format('YYYY-MM-DD') + '&date__lte=' + Moment(end).format('YYYY-MM-DD');
            let url = API_URL + '/user_transactions/' + dateParam;
            if (props.category !== null) {
                const categoryUrlParam = 'category=' + props.category;
                url = url + '&' + categoryUrlParam;
            }
            return await axios.get(url, {
                headers: { Authorization: Authorization }
            });
        } catch (error) {
            console.error(error);
        }
    };
    const loadTransactions = async () => {
        const response = await setDataFromEndpoint();
        if (response) {
            setData(response.data);
        }
    };
    const loadCategories = async () => {
        let url = API_URL + '/user_tags/';
        try {
            let res = await axios.get(url, {
                headers: { Authorization: Authorization }
            });
            if (res) {
                const categoryLookup = res.data.reduce(function (acc, cur, i) {
                    acc[cur.id] = cur.name;
                    return acc;
                }, {});
                setCategories(categoryLookup);
            }
        } catch (error) {
            console.error(error);
        }
    };
    useEffect(() => {
        loadCategories();
        loadTransactions().then(() => setshowloader('false'));
    }, []);
    const handleCellClick = (e) => {
        console.log(e.target.innerHTML);
    };
    return (
        <Box>
            {showloader == 'false' ? (
                <MaterialTable
                    icons={tableIcons}
                    data={data}
                    columns={[
                        { title: 'Transaction Name', field: 'name', editable: 'never' },
                        { title: 'Amount', field: 'value', type: 'numeric', editable: 'never' },
                        {
                            title: 'Category',
                            field: 'tag',
                            lookup: categories
                        },
                        { title: 'Date', field: 'date', type: 'date', editable: 'never' }
                    ]}
                    cellEditable={{
                        onCellEditApproved: (newValue, oldValue, rowData, columnDef) => {
                            return new Promise(async (resolve, reject) => {
                                const url = API_URL + '/user_transactions/' + String(rowData.id) + '/';
                                console.log('newValue: ' + newValue);
                                console.log(rowData);
                                try {
                                    let res = await axios.patch(
                                        url,
                                        { tag: newValue },
                                        {
                                            headers: { Authorization: Authorization }
                                        }
                                    );
                                    if (res.status >= 200 && res.status < 300) {
                                        console.log('success');
                                        await loadTransactions();  // Refresh the list

                                    }
                                } catch (error) {
                                    console.error(error);
                                }
                                setTimeout(resolve, 1000);
                            });
                        }
                    }}
                />
            ) : (
                // <TableContainer
                //     sx={{
                //         height: 600,
                //         width: '100%',
                //         overflowX: 'auto',
                //         position: 'relative',
                //         display: 'block',
                //         maxWidth: '100%',
                //         '& td, & th': { whiteSpace: 'nowrap' }
                //     }}
                // >
                //     <Table
                //         aria-labelledby="tableTitle"
                //         sx={{
                //             height: 'max-content',
                //             '& .MuiTableCell-root:first-child': {
                //                 pl: 2
                //             },
                //             '& .MuiTableCell-root:last-child': {
                //                 pr: 3
                //             }
                //         }}
                //     >
                //         <TransactionTableHead transaction={Transaction} transactionBy={transactionBy} />
                //         <TableBody>
                //             {stableSort(data, getComparator(Transaction, transactionBy)).map((row, index) => {
                //                 const isItemSelected = isSelected(row.id);
                //                 const labelId = `enhanced-table-checkbox-${index}`;
                //
                //                 return (
                //                     <TableRow
                //                         hover
                //                         role="checkbox"
                //                         sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                //                         aria-checked={isItemSelected}
                //                         tabIndex={-1}
                //                         key={row.id}
                //                         selected={isItemSelected}
                //                     >
                //                         {/*<TableCell component="th" id={labelId} scope="row" align="left">*/}
                //                         {/*    <Link color="secondary" component={RouterLink} to="">*/}
                //                         {/*        {row.id}*/}
                //                         {/*    </Link>*/}
                //                         {/*</TableCell>*/}
                //                         <TableCell align="left">{row.date}</TableCell>
                //                         <TableCell align="left">{row.name}</TableCell>
                //                         <TableCell align="left" onClick={handleCellClick}>
                //                             {row.tag}
                //                         </TableCell>
                //                         {/*<TableCell align="left">*/}
                //                         {/*    <TransactionStatus status={1} />*/}
                //                         {/*</TableCell>*/}
                //                         <TableCell align="right">
                //                             <NumberFormat value={row.value} displayType="text" thousandSeparator suffix="₪" />
                //                         </TableCell>
                //                     </TableRow>
                //                 );
                //             })}
                //         </TableBody>
                //     </Table>
                // </TableContainer>
                <Box sx={{ pt: 0.5, width: '100%', height: '100%' }}>
                    {/*<Skeleton height="80%" />*/}
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
