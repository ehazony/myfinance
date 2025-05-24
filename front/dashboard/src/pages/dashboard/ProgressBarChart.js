import React, { useEffect, useState } from 'react';
import styles from './ProgressBarChart.module.css';
import TransactionTable from './TransactionTable';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@mui/material';
function ProgressBarExample({ props }) {
    // console.log(props);
    return (
        // eslint-disable-next-line jsx-a11y/click-events-have-key-events,jsx-a11y/no-static-element-interactions
        <div>
            {/*<header style={{ display: 'flex', justifyContent: 'space-between', paddingRight: '28%' }}>*/}
            {/*    <h2>{props.category}</h2>*/}
            {/*    <h4>*/}
            {/*        <span className={props.percent > 100 ? styles.warning : null}>{String(props.value)} </span>*/}
            {/*        <span> /{String(props.goal)}</span>*/}
            {/*    </h4>*/}
            {/*</header>*/}
            {/*<h3>{String(props.value) + ' / ' + String(props.goal)}</h3>*/}
            <ProgressBar percentage={props.percent} color={props.color} />
        </div>
    );
}

const ProgressBar = (props) => {
    return (
        <div className={styles.progressBar}>
            <Filler percentage={props.percentage} color={props.color} />
        </div>
    );
};
const Filler = (props) => {
    const percentage = Math.min(props.percentage, 100);
    return <div className={styles.filler} style={{ width: `${percentage}%`, background: props.color }} />;
};

export default ProgressBarExample;
