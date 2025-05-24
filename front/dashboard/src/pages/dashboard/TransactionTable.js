import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';

// material-ui
import { Box, Link, Skeleton, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

// third-party
import NumberFormat from 'react-number-format';

// project import
import Dot from 'components/@extended/Dot';
import axios from 'axios';
import Moment from 'moment';
import { useRecoilValue } from 'recoil';
import { authAtom } from '../../_state';

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

export default function TransactionTable() {
    const [Transaction] = useState('asc');
    const [transactionBy] = useState('trackingNo');
    const [selected] = useState([]);
    const [data, getData] = useState([]);
    const token = useRecoilValue(authAtom);
    const [showloader, setshowloader] = useState('true');

    // localStorage.getItem('access_token');
    const API_URL = process.env.REACT_APP_API_URL;

    const Authorization = 'Token ' + token;
    const isSelected = (trackingNo) => selected.indexOf(trackingNo) !== -1;
    function startOfMonth(date) {
        return new Date(date.getFullYear(), date.getMonth(), 1);
    }
    const getDataFromEndpoint = async () => {
        try {
            const dt = new Date();
            const start = startOfMonth(dt).toString();
            const urlParam = '?date__gte=' + Moment(start).format('YYYY-MM-DD');
            return await axios.get(API_URL + '/user_transactions/', {
                headers: { Authorization: Authorization }
            });
        } catch (error) {
            console.error(error);
        }
    };
    const loadData = async () => {
        const response = await getDataFromEndpoint();
        if (response) {
            getData(response.data);
        }
    };
    useEffect(() => {
        loadData();
        setshowloader('false');
    }, []);
    return (
        <Box>
            {showloader == 'false' ? (
                <TableContainer
                    sx={{
                        height: 400,
                        width: '100%',
                        overflowX: 'auto',
                        position: 'relative',
                        display: 'block',
                        maxWidth: '100%',
                        '& td, & th': { whiteSpace: 'nowrap' }
                    }}
                >
                    <Table
                        aria-labelledby="tableTitle"
                        sx={{
                            height: 'max-content',
                            '& .MuiTableCell-root:first-child': {
                                pl: 2
                            },
                            '& .MuiTableCell-root:last-child': {
                                pr: 3
                            }
                        }}
                    >
                        <TransactionTableHead transaction={Transaction} transactionBy={transactionBy} />
                        <TableBody>
                            {stableSort(data, getComparator(Transaction, transactionBy)).map((row, index) => {
                                const isItemSelected = isSelected(row.id);
                                const labelId = `enhanced-table-checkbox-${index}`;

                                return (
                                    <TableRow
                                        hover
                                        role="checkbox"
                                        sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                        aria-checked={isItemSelected}
                                        tabIndex={-1}
                                        key={row.id}
                                        selected={isItemSelected}
                                    >
                                        {/*<TableCell component="th" id={labelId} scope="row" align="left">*/}
                                        {/*    <Link color="secondary" component={RouterLink} to="">*/}
                                        {/*        {row.id}*/}
                                        {/*    </Link>*/}
                                        {/*</TableCell>*/}
                                        <TableCell align="left">{row.name}</TableCell>
                                        <TableCell align="left">{row.tag_name}</TableCell>
                                        {/*<TableCell align="left">*/}
                                        {/*    <TransactionStatus status={1} />*/}
                                        {/*</TableCell>*/}
                                        <TableCell align="right">
                                            <NumberFormat value={row.value} displayType="text" thousandSeparator suffix="₪" />
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            ) : (
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
