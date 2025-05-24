import { useRecoilValue } from 'recoil';
import { Navigate } from 'react-router-dom';

import { authAtom } from '_state';

export { PrivateRoute };

function PrivateRoute({ component: Component, ...props }) {
    const token = useRecoilValue(authAtom);
    console.log('token from authAtom');
    console.log(token);
    return token ? <Component {...props} /> : <Navigate to={'/login'} state={{ from: props.location }} />;
}
