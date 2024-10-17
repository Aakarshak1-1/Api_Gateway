async function authGuard(r) {
    ngx.log(ngx.INFO, "authGuard function called");
    
    let auth = r.headersIn['Authorization'];

    if (!auth) {
        ngx.log(ngx.WARN, "No Authorization header found");
        r.return(401, 'Unauthorized');
        return;
    }

    let jwt_token = null;

    try {
        jwt_token = auth.split(' ')[1];

        if (!jwt_token) {
            ngx.log(ngx.WARN, "No JWT token found in Authorization header");
            r.return(401, 'Unauthorized');
            return;
        }
        
        ngx.log(ngx.INFO, `Fetching token info for token: ${jwt_token.substring(0, 10)}...`);
        
        let response = await ngx.fetch(`http://host.docker.internal:8881/public/auth/token/info`, {
            headers: {
                'Authorization': `Bearer ${jwt_token}`
            }
        });

        ngx.log(ngx.INFO, `Token info response status: ${response.status}`);

        let data = await response.json();

        if (response.status === 200) {
            ngx.log(ngx.INFO, `Authentication successful for user: ${data.data.username}`);
            r.headersOut['X-Auth-User'] = data.data.username;
            r.headersOut['X-Auth-Role'] = data.data.role;
            r.return(200, 'OK');
            return;
        }

        ngx.log(ngx.WARN, `Authentication failed with status: ${response.status}`);
        r.return(response.status, '');

    } catch (err) {
        ngx.log(ngx.ERR, `Error in authGuard: ${err.message}`);
        r.return(500, 'Internal server error from Gateway');
        return;
    }
}

export default { authGuard };