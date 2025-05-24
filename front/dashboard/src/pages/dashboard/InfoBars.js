import { useEffect, useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';

// third-party
import axios from 'axios';
import React, { PureComponent } from 'react';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Box, Card, Grid, List, ListItemButton, ListItemText, Skeleton, Typography } from '@mui/material';
import styles from './ProgressBarChart.module.css';
import ProgressBarExample from './ProgressBarChart';
import { useRecoilValue } from 'recoil';
import { authAtom } from '_state';

// ==============================|| MONTHLY BAR CHART ||============================== //

const InfoBar = () => {
    const theme = useTheme();
    const [showloader, setshowloader] = useState('true');
    const token = useRecoilValue(authAtom);
    const API_URL = process.env.REACT_APP_API_URL;

    const Authorization = 'Token ' + token;

    const [data, getData] = useState([]);
    const listItems = data.map((element) => (
        <div key={element.key}>
            <ListItemButton divider>
                <ListItemText primary={element.key} />
                <Typography variant="h5">{element.value}</Typography>
            </ListItemButton>
        </div>
    ));

    const get_info_data = async () => {
        try {
            return await axios.get(API_URL + '/bank_info/', {
                headers: { Authorization: Authorization }
            });
        } catch (error) {
            console.error(error);
        }
    };
    const loadData = async () => {
        const response = await get_info_data();
        if (response) {
            getData(response.data);
            setshowloader('false');
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    return (
        <div id="info-data">
            <ResponsiveContainer width="95%" height={400}>
                {/*<ReactApexChart options={options} series={setData.graphs.series} type="bar" height={365} />*/}
                {showloader == 'false' ? (
                    <List sx={{ p: 0, '& .MuiListItemButton-root': { py: 2 } }}>{listItems}</List>
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
            </ResponsiveContainer>
        </div>
    );
};

export default InfoBar;
