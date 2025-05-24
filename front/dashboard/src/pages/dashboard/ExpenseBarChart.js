import { useEffect, useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';

// third-party
import axios from 'axios';
import React, { PureComponent } from 'react';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Box, Skeleton } from '@mui/material';
import { useRecoilValue } from 'recoil';
import { authAtom } from '_state';

const data = [
    {
        projectedProfit: 150000,
        AnswerRef: 'one',
        Text: 'Year 1',
        Score: 0,
        RespondentPercentage: 12,
        Rank: 1,
        color: '#96d3e3'
    },
    {
        projectedProfit: 250000,
        AnswerRef: 'two',
        Text: 'Year 2',
        Score: 0,
        RespondentPercentage: 0,
        Rank: 2,
        color: '#6bafc2'
    },
    {
        projectedProfit: 500000,
        AnswerRef: 'three',
        Text: 'Year 3',
        Score: 1,
        RespondentPercentage: 100,
        Rank: 3,
        color: '#017fb1'
    },
    {
        projectedProfit: 750000,
        AnswerRef: 'four',
        Text: 'Year 4',
        Score: 0,
        RespondentPercentage: 16,
        Rank: 4,
        color: '#01678e'
    },
    {
        projectedProfit: 1000000,
        AnswerRef: 'five',
        Text: 'Year 5',
        Score: 0,
        RespondentPercentage: 23,
        Rank: 2,
        color: '#015677'
    }
];

// ==============================|| MONTHLY BAR CHART ||============================== //

export class CustomizedLabel extends React.Component {
    render() {
        const { x, y, fill, value } = this.props;
        return (
            <text x={x} y={y} dy={-4} fontSize="16" fontFamily="sans-serif" fill={fill} textAnchor="middle">
                {value}
            </text>
        );
    }
}

const ExpenseBarChart = () => {
    const theme = useTheme();
    const [showloader, setshowloader] = useState('true');
    const { primary, secondary } = theme.palette.text;
    const info = theme.palette.info.light;
    const token = useRecoilValue(authAtom);
    // localStorage.getItem('access_token');
    const API_URL = process.env.REACT_APP_API_URL;

    const Authorization = 'Token ' + token;
    // const [series] = useState([
    //     {
    //         data: []
    //     }
    // ]);
    const [setData, getData] = useState([]);
    const get_total_month_expenses = async () => {
        try {
            return await axios.get(API_URL + '/total_month_expenses/', {
                headers: { Authorization: Authorization }
            });
        } catch (error) {
            console.error(error);
        }
    };
    const loadData = async () => {
        const response = await get_total_month_expenses();
        if (response) {
            getData(response.data);
            setshowloader('false');
        }
    };
    useEffect(() => {
        loadData();

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [primary, info, secondary]);
    const getIntroOfPage = (label) => {
        return label;
    };

    return (
        <div id="chart">
            <ResponsiveContainer width="95%" height={400}>
                {/*<ReactApexChart options={options} series={setData.graphs.series} type="bar" height={365} />*/}
                {showloader == 'false' ? (
                    <BarChart height={100} data={setData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="text" fontFamily="sans-serif" tickSize dy="25" />
                        <YAxis />
                        <Tooltip />
                        {/*<Legend />*/}
                        <Bar dataKey="value" barSize={170} fontFamily="sans-serif">
                            {setData.map((entry, index) => (
                                <Cell fill={setData[index].color} />
                            ))}
                        </Bar>
                    </BarChart>
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

export default ExpenseBarChart;
