// project import
import Routes from 'routes';
import ThemeCustomization from 'themes';
import ScrollTop from './components/ScrollTop';
import { RecoilRoot } from 'recoil';
import React, { Component } from 'react';

// ==============================|| APP - THEME, ROUTER, LOCAL  ||============================== //

const App = () => (
    <ThemeCustomization>
        <ScrollTop>
            <RecoilRoot>
                <Routes />
            </RecoilRoot>
        </ScrollTop>
    </ThemeCustomization>
);

export default App;
