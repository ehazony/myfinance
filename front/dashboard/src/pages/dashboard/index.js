import React, { useEffect, useState } from 'react';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
// material-ui
import { Box, Grid, Stack, TextField, Typography } from '@mui/material';

// project import
import MainCard from 'components/MainCard';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
// assets
import axios from 'axios';
import MonthSpendingChart from './MonthSpendingChart';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import InfoBar from './InfoBars';
import { useRecoilValue } from 'recoil';
import { authAtom } from '_state';
// avatar style
const avatarSX = {
    width: 36,
    height: 36,
    fontSize: '1rem'
};

// action style
const actionSX = {
    mt: 0.75,
    ml: 1,
    top: 'auto',
    right: 'auto',
    alignSelf: 'flex-start',
    transform: 'none'
};

// sales report status
const status = [
    {
        value: 'today',
        label: 'Today'
    },
    {
        value: 'month',
        label: 'This Month'
    },
    {
        value: 'year',
        label: 'This Year'
    }
];

// ==============================|| DASHBOARD - DEFAULT ||============================== //

const DashboardDefault = () => {
    const [value, setValue] = useState('today');
    const [slot, setSlot] = useState('week');
    const [date, setDate] = useState(new Date());

    // Update only the month of the date
    const handleMonthChange = (newValue) => {
        if (newValue) {
            const updatedDate = new Date(date);
            // newValue is a Date object, so we use its month
            updatedDate.setMonth(newValue.getMonth());
            setDate(updatedDate);
        }
    };

    // Update only the year of the date
    const handleYearChange = (newValue) => {
        if (newValue) {
            const updatedDate = new Date(date);
            updatedDate.setFullYear(newValue.getFullYear());
            setDate(updatedDate);
        }
    };
    const [setData, getData] = useState({
        average_expenses: '',
        average_income: '',
        number_of_months: '',
        average_bank_expenses: '',
        graphs: { series: '', date: '' }
    });
    const token = useRecoilValue(authAtom);
    // localStorage.getItem('access_token');
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
        <div>
            <Grid container rowSpacing={8.5} columnSpacing={6.75} justifyContent={'center'}>
                {/* row 1 */}
                {/*<Grid item xs={12} sx={{ mb: -2.25 }}>*/}
                {/*    <Typography variant="h5">Dashboard</Typography>*/}
                {/*</Grid>*/}
                {/*<Grid item xs={12} sm={6} md={4} lg={3}>*/}
                {/*    <AnalyticEcommerce title="Total Page Views" count="4,42,236" percentage={59.3} extra="35,000" />*/}
                {/*</Grid>*/}
                {/*<Grid item xs={12} sm={6} md={4} lg={3}>*/}
                {/*    <AnalyticEcommerce title="Total Users" count="78,250" percentage={70.5} extra="8,900" />*/}
                {/*</Grid>*/}
                {/*<Grid item xs={12} sm={6} md={4} lg={3}>*/}
                {/*    <AnalyticEcommerce title="Total Order" count="18,800" percentage={27.4} isLoss color="warning" extra="1,943" />*/}
                {/*</Grid>*/}
                {/*<Grid item xs={12} sm={6} md={4} lg={3}>*/}
                {/*    <AnalyticEcommerce title="Total Sales" count="$35,078" percentage={27.4} isLoss color="warning" extra="$20,395" />*/}
                {/*</Grid>*/}

                {/*<Grid item md={8} sx={{ display: { sm: 'none', md: 'block', lg: 'none' } }} />*/}

                {/* row 2 */}
                <Grid item xs={12} md={5} lg={6}>
                    <Grid container alignItems="center" justifyContent="space-between">
                        <Grid item>
                            <Typography variant="h5">Monthly Spending</Typography>
                        </Grid>
                        <Grid item>
                            <Stack direction="row" alignItems="center" spacing={0}>
                                <LocalizationProvider dateAdapter={AdapterDateFns}>
                                    {/* Month Picker */}
                                    <DatePicker
                                        views={['year']}
                                        label="Year"
                                        disableFuture
                                        value={date}
                                        onChange={handleYearChange}
                                        renderInput={(params) => <TextField {...params} helperText={null} />}
                                    />
                                    <DatePicker
                                        views={['month']}
                                        inputFormat="MMMM"
                                        label="Month"
                                        openTo="month"
                                        disableFuture
                                        value={date}
                                        onChange={handleMonthChange}
                                        renderInput={(params) => <TextField {...params} helperText={null} />}
                                    />
                                    {/* Year Picker */}
                                </LocalizationProvider>
                            </Stack>
                        </Grid>
                    </Grid>
                    <MainCard sx={{ mt: 2 }} content={false}>
                        <Box sx={{ p: 3, pb: 0, overflowY: 'scroll', overflowX: 'hidden', maxHeight: '600px' }}>
                            <Stack spacing={2}>
                                <MonthSpendingChart date={date} key={date.toString()} />
                            </Stack>
                        </Box>
                    </MainCard>
                </Grid>
                <Grid item xs={12} md={5} lg={3}>
                    <Grid container alignItems="center" justifyContent="space-between">
                        <Grid item>
                            <Typography variant="h5">Bank Summery</Typography>
                        </Grid>
                        <Grid item />
                    </Grid>
                    <MainCard sx={{ mt: 2 }} content={false}>
                        <InfoBar></InfoBar>
                        {/*<ReportAreaChart />*/}
                    </MainCard>
                </Grid>
                {/*<Grid item xs={4} md={5} lg={4}>*/}
                {/*    <Grid container alignItems="center" justifyContent="space-between">*/}
                {/*        <Grid item>*/}
                {/*            <Typography variant="h5">Spent By Month</Typography>*/}
                {/*        </Grid>*/}
                {/*        <Grid item />*/}
                {/*    </Grid>*/}
                {/*    <MainCard sx={{ mt: 2, py: 4 }} content={false}>*/}
                {/*        <ExpenseBarChart spacing={2} />*/}
                {/*    </MainCard>*/}
                {/*</Grid>*/}

                {/* row 3 */}
                {/* row 4 */}
                {/*<Grid item xs={12} md={7} lg={8}>*/}
                {/*    <Grid container alignItems="center" justifyContent="space-between">*/}
                {/*        <Grid item>*/}
                {/*            <Typography variant="h5">Sales Report</Typography>*/}
                {/*        </Grid>*/}
                {/*        <Grid item>*/}
                {/*            <TextField*/}
                {/*                id="standard-select-currency"*/}
                {/*                size="small"*/}
                {/*                select*/}
                {/*                value={value}*/}
                {/*                onChange={(e) => setValue(e.target.value)}*/}
                {/*                sx={{ '& .MuiInputBase-input': { py: 0.5, fontSize: '0.875rem' } }}*/}
                {/*            >*/}
                {/*                {status.map((option) => (*/}
                {/*                    <MenuItem key={option.value} value={option.value}>*/}
                {/*                        {option.label}*/}
                {/*                    </MenuItem>*/}
                {/*                ))}*/}
                {/*            </TextField>*/}
                {/*        </Grid>*/}
                {/*    </Grid>*/}
                {/*    <MainCard sx={{ mt: 1.75 }}>*/}
                {/*        <Stack spacing={1.5} sx={{ mb: -12 }}>*/}
                {/*            <Typography variant="h6" color="secondary">*/}
                {/*                Net Profit*/}
                {/*            </Typography>*/}
                {/*            <Typography variant="h4">$1560</Typography>*/}
                {/*        </Stack>*/}
                {/*        <SalesColumnChart />*/}
                {/*    </MainCard>*/}
                {/*</Grid>*/}
                {/*<Grid item xs={12} md={5} lg={4}>*/}
                {/*    <Grid container alignItems="center" justifyContent="space-between">*/}
                {/*        <Grid item>*/}
                {/*            <Typography variant="h5">Transaction History</Typography>*/}
                {/*        </Grid>*/}
                {/*        <Grid item />*/}
                {/*    </Grid>*/}
                {/*    <MainCard sx={{ mt: 2 }} content={false}>*/}
                {/*        <List*/}
                {/*            component="nav"*/}
                {/*            sx={{*/}
                {/*                px: 0,*/}
                {/*                py: 0,*/}
                {/*                '& .MuiListItemButton-root': {*/}
                {/*                    py: 1.5,*/}
                {/*                    '& .MuiAvatar-root': avatarSX,*/}
                {/*                    '& .MuiListItemSecondaryAction-root': { ...actionSX, position: 'relative' }*/}
                {/*                }*/}
                {/*            }}*/}
                {/*        >*/}
                {/*            <ListItemButton divider>*/}
                {/*                <ListItemAvatar>*/}
                {/*                    <Avatar*/}
                {/*                        sx={{*/}
                {/*                            color: 'success.main',*/}
                {/*                            bgcolor: 'success.lighter'*/}
                {/*                        }}*/}
                {/*                    >*/}
                {/*                        <GiftOutlined />*/}
                {/*                    </Avatar>*/}
                {/*                </ListItemAvatar>*/}
                {/*                <ListItemText primary={<Typography variant="subtitle1">Order #002434</Typography>} secondary="Today, 2:00 AM" />*/}
                {/*                <ListItemSecondaryAction>*/}
                {/*                    <Stack alignItems="flex-end">*/}
                {/*                        <Typography variant="subtitle1" noWrap>*/}
                {/*                            + $1,430*/}
                {/*                        </Typography>*/}
                {/*                        <Typography variant="h6" color="secondary" noWrap>*/}
                {/*                            78%*/}
                {/*                        </Typography>*/}
                {/*                    </Stack>*/}
                {/*                </ListItemSecondaryAction>*/}
                {/*            </ListItemButton>*/}
                {/*            <ListItemButton divider>*/}
                {/*                <ListItemAvatar>*/}
                {/*                    <Avatar*/}
                {/*                        sx={{*/}
                {/*                            color: 'primary.main',*/}
                {/*                            bgcolor: 'primary.lighter'*/}
                {/*                        }}*/}
                {/*                    >*/}
                {/*                        <MessageOutlined />*/}
                {/*                    </Avatar>*/}
                {/*                </ListItemAvatar>*/}
                {/*                <ListItemText*/}
                {/*                    primary={<Typography variant="subtitle1">Order #984947</Typography>}*/}
                {/*                    secondary="5 August, 1:45 PM"*/}
                {/*                />*/}
                {/*                <ListItemSecondaryAction>*/}
                {/*                    <Stack alignItems="flex-end">*/}
                {/*                        <Typography variant="subtitle1" noWrap>*/}
                {/*                            + $302*/}
                {/*                        </Typography>*/}
                {/*                        <Typography variant="h6" color="secondary" noWrap>*/}
                {/*                            8%*/}
                {/*                        </Typography>*/}
                {/*                    </Stack>*/}
                {/*                </ListItemSecondaryAction>*/}
                {/*            </ListItemButton>*/}
                {/*            <ListItemButton>*/}
                {/*                <ListItemAvatar>*/}
                {/*                    <Avatar*/}
                {/*                        sx={{*/}
                {/*                            color: 'error.main',*/}
                {/*                            bgcolor: 'error.lighter'*/}
                {/*                        }}*/}
                {/*                    >*/}
                {/*                        <SettingOutlined />*/}
                {/*                    </Avatar>*/}
                {/*                </ListItemAvatar>*/}
                {/*                <ListItemText primary={<Typography variant="subtitle1">Order #988784</Typography>} secondary="7 hours ago" />*/}
                {/*                <ListItemSecondaryAction>*/}
                {/*                    <Stack alignItems="flex-end">*/}
                {/*                        <Typography variant="subtitle1" noWrap>*/}
                {/*                            + $682*/}
                {/*                        </Typography>*/}
                {/*                        <Typography variant="h6" color="secondary" noWrap>*/}
                {/*                            16%*/}
                {/*                        </Typography>*/}
                {/*                    </Stack>*/}
                {/*                </ListItemSecondaryAction>*/}
                {/*            </ListItemButton>*/}
                {/*        </List>*/}
                {/*    </MainCard>*/}
                {/*    <MainCard sx={{ mt: 2 }}>*/}
                {/*        <Stack spacing={3}>*/}
                {/*            <Grid container justifyContent="space-between" alignItems="center">*/}
                {/*                <Grid item>*/}
                {/*                    <Stack>*/}
                {/*                        <Typography variant="h5" noWrap>*/}
                {/*                            Help & Support Chat*/}
                {/*                        </Typography>*/}
                {/*                        <Typography variant="caption" color="secondary" noWrap>*/}
                {/*                            Typical replay within 5 min*/}
                {/*                        </Typography>*/}
                {/*                    </Stack>*/}
                {/*                </Grid>*/}
                {/*                <Grid item>*/}
                {/*                    <AvatarGroup sx={{ '& .MuiAvatar-root': { width: 32, height: 32 } }}>*/}
                {/*                        <Avatar alt="Remy Sharp" src={avatar1} />*/}
                {/*                        <Avatar alt="Travis Howard" src={avatar2} />*/}
                {/*                        <Avatar alt="Cindy Baker" src={avatar3} />*/}
                {/*                        <Avatar alt="Agnes Walker" src={avatar4} />*/}
                {/*                    </AvatarGroup>*/}
                {/*                </Grid>*/}
                {/*            </Grid>*/}
                {/*            <Button size="small" variant="contained" sx={{ textTransform: 'capitalize' }}>*/}
                {/*                Need Help?*/}
                {/*            </Button>*/}
                {/*        </Stack>*/}
                {/*    </MainCard>*/}
                {/*</Grid>*/}
            </Grid>
            <Fab color="primary" aria-label="add" style={{ right: 70, bottom: 70, position: 'fixed' }}>
                <AddIcon />
            </Fab>
        </div>
    );
};

export default DashboardDefault;
