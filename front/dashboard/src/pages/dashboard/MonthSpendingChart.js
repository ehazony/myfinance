import { useEffect, useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import Moment from 'moment';
// third-party
import axios from 'axios';
import React, { PureComponent } from 'react';
import MoreVertSharpIcon from '@mui/icons-material/MoreVertSharp';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import {
    Box,
    Button,
    Card,
    CardHeader,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Grid,
    Skeleton,
    TextField,
    IconButton,
    Menu,
    MenuItem
} from '@mui/material';
import ProgressBarExample from './ProgressBarChart';
import styles from './ProgressBarChart.module.css';
import TransactionTable from '../transactions/TransactionTable';
import { authAtom } from '_state';
import { useRecoilValue } from 'recoil';

const MonthSpendingChart = ({ date }) => {
    const theme = useTheme();
    const [showloader, setshowloader] = useState('true');
    const { primary, secondary } = theme.palette.text;
    const info = theme.palette.info.light;
    const token = useRecoilValue(authAtom);
    const API_URL = process.env.REACT_APP_API_URL;

    const Authorization = 'Token ' + token;
    const [data, getData] = useState([]);
    const [openPopup, setOpenPopup] = useState(false);
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [menuCategory, setMenuCategory] = React.useState(null);
    const handleClick = (param) => (event) => {
        setMenuCategory(param);
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
    const handleClosePopup = () => {
        setOpenPopup(false);
    };
    const handleOpenPopup = () => {
        setOpenPopup(true);
    };
    const getDataFromEndpoint = async (category) => {
        try {
            let endpoint = API_URL + '/month_category/?' + 'month=' + Moment(date).format('YYYYMM');
            if (category !== undefined && category !== null) {
                endpoint = endpoint + '&category=' + category;
            }
            return await axios.get(endpoint, {
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
            setshowloader('false');
        }
    };
    useEffect(() => {
        loadData();
        console.log(openPopup);
    }, [primary, info, secondary, openPopup]);
    const open = Boolean(anchorEl);

    const handleTransactionMenu = () => {
        // call get category transactions
        handleOpenPopup();
        handleClose();
    };

    const listItems = data.map((element, index) => (
        <Grid item xs={0} sm={4} md={4} m={-1} key={index}>
            <Card className={styles.card}>
                <CardHeader
                    title={element.category}
                    subheader={String(element.value) + '/' + String(element.goal)}
                    action={
                        <IconButton>
                            <MoreVertSharpIcon key={element.key} onClick={(e) => handleClick(element.key)(e)} />
                        </IconButton>
                    }
                ></CardHeader>
                <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
                    <MenuItem onClick={handleTransactionMenu}>Transactions</MenuItem>
                </Menu>
                <ProgressBarExample props={element} />
            </Card>
        </Grid>
    ));
    return (
        <div id="chart">
            {showloader == 'false' ? (
                <Grid container direction={'column'} justify="center" paddingLeft={{ xs: 1, sm: 2, mg: 2, lg: 4 }} spacing={6}>
                    {listItems}
                    <Dialog open={openPopup} onClose={handleClosePopup}>
                        <DialogTitle>Transactions</DialogTitle>
                        <DialogContent>
                            <DialogContentText>Current Month Category Transactions.</DialogContentText>
                            <TransactionTable category={menuCategory} date={date} />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleClosePopup}>Close</Button>
                        </DialogActions>
                    </Dialog>
                </Grid>
            ) : (
                <Box sx={{ pt: 0.5, width: 1, height: 1 }}>
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
        </div>
    );
};

export default MonthSpendingChart;
