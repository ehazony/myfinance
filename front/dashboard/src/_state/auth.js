import { atom } from 'recoil';
import Cookies from 'universal-cookie';

const cookies = new Cookies();

const authAtom = atom({
    key: 'token',
    // get initial state from local storage to enable user to stay logged in
    default: cookies.get('token')
});

export { authAtom };
