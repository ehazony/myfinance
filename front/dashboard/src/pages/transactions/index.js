import React, { useEffect, useState } from 'react';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
// material-ui
import { Box, Button, Grid, Stack, TextField, Typography } from '@mui/material';

// project import
import TransactionTable from './TransactionTable';
import MainCard from 'components/MainCard';
// assets
import axios from 'axios';
import { DatePicker, LocalizationProvider, MonthPicker, StaticDatePicker } from '@mui/lab';
import { useRecoilValue } from 'recoil';
import { authAtom } from '_state';
// avatar style

// action style

// sales report status

// ==============================|| DASHBOARD - DEFAULT ||============================== //

const DashboardDefault = () => {
    const [value, setValue] = useState('today');
    const [month, setMonth] = useState(new Date());
    const [slot, setSlot] = useState('week');

    const [setData, getData] = useState({
        average_expenses: '',
        average_income: '',
        number_of_months: '',
        average_bank_expenses: '',
        graphs: { series: '', date: '' }
    });
    const token = useRecoilValue(authAtom);
    const API_URL = process.env.REACT_APP_API_URL;

    const Authorization = 'Token ' + token;
    const getSummeryData = async () => {
        try {
            return await axios.get(API_URL + '/summery_widgets/', {
                headers: { Authorization: Authorization }
            });
        } catch (error) {
            console.error(error);
        }
    };

    const GethandleClick = async () => {
        const response = await getSummeryData();
        if (response) {
            getData(response.data);
            // setshowloader('false');
        }
    };

    useEffect(() => {
        GethandleClick();
    }, []);
    return (
        <Grid container rowSpacing={8.5} columnSpacing={6.75} justifyContent={'center'}>
            <Grid item xs={12} md={7} lg={8}>
                <Grid container alignItems="center" justifyContent="space-between">
                    <Grid item>
                        <Typography variant="h5">Recent Transactions</Typography>
                    </Grid>
                    <Grid item />
                </Grid>
                <MainCard sx={{ mt: 2 }} content={false}>
                    <TransactionTable category={null} date={new Date(2023, 0, 1)} />
                </MainCard>
            </Grid>
        </Grid>
    );
};

export default DashboardDefault;
